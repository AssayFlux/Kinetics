use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use sqlx::{PgPool, Row};
use thiserror::Error;
use uuid::Uuid;

#[derive(Debug, Error)]
pub enum RuntimeStoreError {
    #[error("database operation failed")]
    Database(#[from] sqlx::Error),
    #[error("job not found")]
    NotFound,
    #[error("tenant quota exceeded")]
    QuotaExceeded,
    #[error("job state conflict")]
    Conflict,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct RuntimeJob {
    pub id: Uuid,
    pub tenant_id: String,
    pub state: String,
    pub payload: serde_json::Value,
    pub attempt: i32,
    pub max_attempts: i32,
    pub max_runtime_seconds: i64,
    pub max_memory_bytes: i64,
    pub max_cpu_millis: i32,
    pub cancel_requested: bool,
    pub lease_owner: Option<String>,
    pub lease_expires_at: Option<DateTime<Utc>>,
}

#[derive(Clone, Copy, Debug)]
pub struct JobSubmissionLimits {
    pub max_runtime_seconds: i64,
    pub max_memory_bytes: i64,
    pub max_cpu_millis: i32,
    pub max_active_jobs: i64,
}

#[derive(Clone)]
pub struct PostgresRuntimeStore {
    pool: PgPool,
}

impl PostgresRuntimeStore {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }

    pub async fn submit(
        &self,
        tenant: &str,
        idempotency_key: &str,
        payload: serde_json::Value,
        limits: JobSubmissionLimits,
    ) -> Result<RuntimeJob, RuntimeStoreError> {
        if tenant.trim().is_empty()
            || idempotency_key.trim().is_empty()
            || limits.max_runtime_seconds <= 0
            || limits.max_memory_bytes <= 0
            || limits.max_cpu_millis <= 0
            || limits.max_active_jobs <= 0
        {
            return Err(RuntimeStoreError::Conflict);
        }
        let mut tx = self.pool.begin().await?;
        sqlx::query("SELECT pg_advisory_xact_lock(hashtextextended($1, 0))")
            .bind(tenant)
            .execute(&mut *tx)
            .await?;
        let existing =
            sqlx::query("SELECT * FROM kinetics_jobs WHERE tenant_id=$1 AND idempotency_key=$2")
                .bind(tenant)
                .bind(idempotency_key)
                .fetch_optional(&mut *tx)
                .await?;
        if let Some(row) = existing {
            let job = row_to_job(&row);
            if job.payload != payload
                || job.max_runtime_seconds != limits.max_runtime_seconds
                || job.max_memory_bytes != limits.max_memory_bytes
                || job.max_cpu_millis != limits.max_cpu_millis
            {
                return Err(RuntimeStoreError::Conflict);
            }
            tx.commit().await?;
            return Ok(job);
        }
        let active: i64 = sqlx::query_scalar(
            "SELECT count(*) FROM kinetics_jobs WHERE tenant_id=$1 AND state IN ('queued','running')"
        ).bind(tenant).fetch_one(&mut *tx).await?;
        if active >= limits.max_active_jobs {
            return Err(RuntimeStoreError::QuotaExceeded);
        }
        let id = Uuid::new_v4();
        let row = sqlx::query(
            "INSERT INTO kinetics_jobs
             (id, tenant_id, idempotency_key, payload, state, max_runtime_seconds, max_memory_bytes, max_cpu_millis)
             VALUES ($1,$2,$3,$4,'queued',$5,$6,$7) RETURNING *"
        ).bind(id).bind(tenant).bind(idempotency_key).bind(payload)
         .bind(limits.max_runtime_seconds)
        .bind(limits.max_memory_bytes)
        .bind(limits.max_cpu_millis)
         .fetch_one(&mut *tx).await?;
        tx.commit().await?;
        Ok(row_to_job(&row))
    }

    /// Atomically claim one queued job or an expired lease. SKIP LOCKED permits
    /// multiple independent workers to compete without double-claiming.
    pub async fn claim(
        &self,
        worker: &str,
        lease_seconds: i64,
    ) -> Result<Option<RuntimeJob>, RuntimeStoreError> {
        sqlx::query(
            "UPDATE kinetics_jobs SET state='failed', lease_owner=NULL, lease_expires_at=NULL, updated_at=now()
             WHERE state='running' AND lease_expires_at < now() AND attempt >= max_attempts"
        ).execute(&self.pool).await?;
        let row = sqlx::query(
            "WITH candidate AS (
               SELECT id FROM kinetics_jobs
               WHERE cancel_requested = false
                 AND ((state='queued' AND attempt < max_attempts
                       AND (next_attempt_at IS NULL OR next_attempt_at <= now()))
                      OR (state='running' AND lease_expires_at < now() AND attempt < max_attempts))
               ORDER BY created_at
               FOR UPDATE SKIP LOCKED LIMIT 1
             )
             UPDATE kinetics_jobs j
             SET state='running', lease_owner=$1,
                 lease_expires_at=now() + ($2 * interval '1 second'),
                 attempt=j.attempt+1,
                 started_at=COALESCE(j.started_at, now()), updated_at=now()
             FROM candidate c WHERE j.id=c.id RETURNING j.*",
        )
        .bind(worker)
        .bind(lease_seconds.max(5))
        .fetch_optional(&self.pool)
        .await?;
        Ok(row.as_ref().map(row_to_job))
    }

    pub async fn heartbeat(
        &self,
        id: Uuid,
        worker: &str,
        lease_seconds: i64,
    ) -> Result<bool, RuntimeStoreError> {
        let result = sqlx::query(
            "UPDATE kinetics_jobs SET lease_expires_at=now()+($3 * interval '1 second'), updated_at=now()
             WHERE id=$1 AND lease_owner=$2 AND state='running' AND cancel_requested=false
               AND lease_expires_at > now()"
        ).bind(id).bind(worker).bind(lease_seconds.max(5))
         .execute(&self.pool).await?;
        Ok(result.rows_affected() == 1)
    }

    pub async fn cancellation_requested(
        &self,
        id: Uuid,
        worker: &str,
    ) -> Result<bool, RuntimeStoreError> {
        let value = sqlx::query_scalar(
            "SELECT cancel_requested FROM kinetics_jobs WHERE id=$1 AND lease_owner=$2",
        )
        .bind(id)
        .bind(worker)
        .fetch_optional(&self.pool)
        .await?;
        value.ok_or(RuntimeStoreError::NotFound)
    }

    pub async fn request_cancel(&self, tenant: &str, id: Uuid) -> Result<(), RuntimeStoreError> {
        let result = sqlx::query(
            "UPDATE kinetics_jobs SET cancel_requested=true,
             state=CASE WHEN state='queued' THEN 'cancelled' ELSE state END, updated_at=now()
             WHERE id=$1 AND tenant_id=$2 AND state IN ('queued','running')",
        )
        .bind(id)
        .bind(tenant)
        .execute(&self.pool)
        .await?;
        if result.rows_affected() == 0 {
            return Err(RuntimeStoreError::NotFound);
        }
        Ok(())
    }

    pub async fn finish(
        &self,
        id: Uuid,
        worker: &str,
        success: bool,
    ) -> Result<(), RuntimeStoreError> {
        let result = sqlx::query(
            "UPDATE kinetics_jobs
             SET state=CASE
                   WHEN cancel_requested THEN 'cancelled'
                   WHEN $3 THEN 'succeeded'
                   WHEN attempt < max_attempts THEN 'queued'
                   ELSE 'failed'
                 END,
                 next_attempt_at=CASE WHEN NOT $3 AND NOT cancel_requested AND attempt < max_attempts
                                      THEN now() + (LEAST(300::double precision, (5 * power(2, GREATEST(attempt - 1, 0)))::double precision) * interval '1 second')
                                      ELSE NULL END,
                 lease_owner=NULL, lease_expires_at=NULL, updated_at=now()
             WHERE id=$1 AND lease_owner=$2 AND state='running'"
        ).bind(id).bind(worker).bind(success).execute(&self.pool).await?;
        if result.rows_affected() == 0 {
            return Err(RuntimeStoreError::Conflict);
        }
        Ok(())
    }

    pub async fn finish_cancelled(&self, id: Uuid, worker: &str) -> Result<(), RuntimeStoreError> {
        let result = sqlx::query(
            "UPDATE kinetics_jobs SET state='cancelled', lease_owner=NULL, lease_expires_at=NULL, updated_at=now()
             WHERE id=$1 AND lease_owner=$2 AND state='running' AND cancel_requested=true"
        ).bind(id).bind(worker).execute(&self.pool).await?;
        if result.rows_affected() == 0 {
            return Err(RuntimeStoreError::Conflict);
        }
        Ok(())
    }

    pub async fn get(&self, tenant: &str, id: Uuid) -> Result<RuntimeJob, RuntimeStoreError> {
        let row = sqlx::query("SELECT * FROM kinetics_jobs WHERE id=$1 AND tenant_id=$2")
            .bind(id)
            .bind(tenant)
            .fetch_optional(&self.pool)
            .await?
            .ok_or(RuntimeStoreError::NotFound)?;
        Ok(row_to_job(&row))
    }
}

fn row_to_job(row: &sqlx::postgres::PgRow) -> RuntimeJob {
    RuntimeJob {
        id: row.get("id"),
        tenant_id: row.get("tenant_id"),
        state: row.get("state"),
        payload: row.get("payload"),
        attempt: row.get("attempt"),
        max_attempts: row.get("max_attempts"),
        max_runtime_seconds: row.get("max_runtime_seconds"),
        max_memory_bytes: row.get("max_memory_bytes"),
        max_cpu_millis: row.get("max_cpu_millis"),
        cancel_requested: row.get("cancel_requested"),
        lease_owner: row.get("lease_owner"),
        lease_expires_at: row.get("lease_expires_at"),
    }
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct AppendAuditEvent {
    pub event_id: Uuid,
    pub tenant_id: String,
    pub actor_subject: String,
    pub action: String,
    pub resource_type: String,
    pub resource_id: String,
    pub outcome: String,
    pub correlation_id: String,
    pub occurred_at: DateTime<Utc>,
}

#[derive(Clone)]
pub struct AppendOnlyAuditStore {
    pool: PgPool,
}

impl AppendOnlyAuditStore {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }

    pub async fn append(&self, event: &AppendAuditEvent) -> Result<String, RuntimeStoreError> {
        let mut tx = self.pool.begin().await?;
        sqlx::query("SELECT pg_advisory_xact_lock(729104)")
            .execute(&mut *tx)
            .await?;
        let previous: Option<String> = sqlx::query_scalar(
            "SELECT event_hash FROM kinetics_audit_events ORDER BY sequence_id DESC LIMIT 1",
        )
        .fetch_optional(&mut *tx)
        .await?;
        let canonical =
            serde_json::to_vec(&(event, previous.as_deref())).expect("serializable audit event");
        let hash = Sha256::digest(canonical)
            .iter()
            .map(|b| format!("{b:02x}"))
            .collect::<String>();
        sqlx::query(
            "INSERT INTO kinetics_audit_events
             (event_id,tenant_id,actor_subject,action,resource_type,resource_id,outcome,correlation_id,occurred_at,previous_hash,event_hash)
             VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)"
        ).bind(event.event_id).bind(&event.tenant_id).bind(&event.actor_subject)
         .bind(&event.action).bind(&event.resource_type).bind(&event.resource_id)
         .bind(&event.outcome).bind(&event.correlation_id).bind(event.occurred_at)
         .bind(previous).bind(&hash).execute(&mut *tx).await?;
        tx.commit().await?;
        Ok(hash)
    }
}
