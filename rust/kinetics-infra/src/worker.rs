use async_trait::async_trait;
use tokio::{
    task::JoinHandle,
    time::{sleep, timeout, Duration},
};
use tokio_util::sync::CancellationToken;
use uuid::Uuid;

use crate::postgres::{PostgresRuntimeStore, RuntimeJob, RuntimeStoreError};

#[async_trait]
pub trait JobExecutor: Send + Sync + 'static {
    async fn execute(
        &self,
        job: &RuntimeJob,
        cancellation: CancellationToken,
    ) -> Result<(), String>;
}

pub struct WorkerRuntime<E> {
    store: PostgresRuntimeStore,
    executor: E,
    worker_id: String,
    lease_seconds: i64,
}

impl<E: JobExecutor> WorkerRuntime<E> {
    pub fn new(
        store: PostgresRuntimeStore,
        executor: E,
        worker_id: String,
        lease_seconds: i64,
    ) -> Self {
        Self {
            store,
            executor,
            worker_id,
            lease_seconds: lease_seconds.max(15),
        }
    }

    pub async fn run_once(&self) -> Result<bool, RuntimeStoreError> {
        let Some(job) = self
            .store
            .claim(&self.worker_id, self.lease_seconds)
            .await?
        else {
            return Ok(false);
        };
        let cancellation = CancellationToken::new();
        let heartbeat = self.start_heartbeat(job.id, cancellation.clone());
        let execution = timeout(
            Duration::from_secs(job.max_runtime_seconds.max(1) as u64),
            self.executor.execute(&job, cancellation.clone()),
        )
        .await;
        cancellation.cancel();
        heartbeat.abort();

        if self
            .store
            .cancellation_requested(job.id, &self.worker_id)
            .await
            .unwrap_or(false)
        {
            // Cancellation is a terminal result; a worker must never publish a
            // successful result after the API has accepted cancellation.
            self.store.finish_cancelled(job.id, &self.worker_id).await?;
        } else {
            self.store
                .finish(job.id, &self.worker_id, matches!(execution, Ok(Ok(()))))
                .await?;
        }
        Ok(true)
    }

    fn start_heartbeat(&self, job_id: Uuid, cancellation: CancellationToken) -> JoinHandle<()> {
        let store = self.store.clone();
        let worker_id = self.worker_id.clone();
        let interval = Duration::from_secs((self.lease_seconds / 3).max(5) as u64);
        let lease = self.lease_seconds;
        tokio::spawn(async move {
            loop {
                tokio::select! {
                    _ = cancellation.cancelled() => break,
                    _ = sleep(interval) => {
                        match store.heartbeat(job_id, &worker_id, lease).await {
                            Ok(true) => {},
                            _ => { cancellation.cancel(); break; }
                        }
                    }
                }
            }
        })
    }

    pub async fn run_forever(&self, idle_delay: Duration) -> Result<(), RuntimeStoreError> {
        loop {
            if !self.run_once().await? {
                sleep(idle_delay).await;
            }
        }
    }
}
