use std::{env, time::Duration};

use async_trait::async_trait;
use sqlx::postgres::PgPoolOptions;
use tokio_util::sync::CancellationToken;

use kinetics_infra::{
    cloud_secrets::AwsSecretProvider,
    postgres::{PostgresRuntimeStore, RuntimeJob},
    worker::{JobExecutor, WorkerRuntime},
};

struct ConfiguredExecutor;

#[async_trait]
impl JobExecutor for ConfiguredExecutor {
    async fn execute(
        &self,
        job: &RuntimeJob,
        cancellation: CancellationToken,
    ) -> Result<(), String> {
        // Dispatch is deliberately allow-listed. The concrete scientific task
        // runner is injected by the Kinetics execution package, not arbitrary
        // shell commands or user-supplied executable paths.
        let task = job
            .payload
            .get("task")
            .and_then(|v| v.as_str())
            .unwrap_or("")
            .to_owned();
        match task.as_str() {
            "kinetics.noop_healthcheck" => {
                if cancellation.is_cancelled() {
                    return Err("cancelled".into());
                }
                Ok(())
            }
            _ => Err("unsupported_task_handler".into()),
        }
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt()
        .json()
        .with_env_filter("info")
        .init();
    let secrets = AwsSecretProvider::from_default_identity().await;
    let secret_id = env::var("KINETICS_DATABASE_SECRET_ID")?;
    let secret = secrets.get(&secret_id).await?;
    let database_url = if secret.starts_with("postgres://") || secret.starts_with("postgresql://") {
        secret
    } else {
        let value: serde_json::Value = serde_json::from_str(&secret)?;
        let mut url = url::Url::parse("postgres://localhost/postgres")?;
        url.set_username(value["username"].as_str().ok_or("missing username")?)?;
        url.set_password(Some(value["password"].as_str().ok_or("missing password")?))
            .map_err(|_| "invalid password")?;
        url.set_host(Some(value["host"].as_str().ok_or("missing host")?))?;
        if let Some(port) = value["port"].as_u64() {
            url.set_port(Some(port as u16))
                .map_err(|_| "invalid port")?;
        }
        url.set_path(value["dbname"].as_str().unwrap_or("kinetics"));
        url.to_string()
    };
    let pool = PgPoolOptions::new()
        .max_connections(10)
        .connect(&database_url)
        .await?;
    let store = PostgresRuntimeStore::new(pool);
    let worker_id =
        env::var("HOSTNAME").unwrap_or_else(|_| format!("worker-{}", uuid::Uuid::new_v4()));
    let runtime = WorkerRuntime::new(store, ConfiguredExecutor, worker_id, 60);
    runtime.run_forever(Duration::from_secs(2)).await?;
    Ok(())
}
