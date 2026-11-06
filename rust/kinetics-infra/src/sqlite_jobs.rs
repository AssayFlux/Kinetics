use std::path::Path;

use crate::jobs::{Job, JobError, JobState, ResourceLimits};
use rusqlite::{params, Connection, OptionalExtension};

#[derive(Debug)]
pub enum SqliteJobError {
    Sqlite(rusqlite::Error),
    Serialization(serde_json::Error),
    Job(JobError),
}

impl From<rusqlite::Error> for SqliteJobError {
    fn from(value: rusqlite::Error) -> Self {
        Self::Sqlite(value)
    }
}

impl From<serde_json::Error> for SqliteJobError {
    fn from(value: serde_json::Error) -> Self {
        Self::Serialization(value)
    }
}

impl From<JobError> for SqliteJobError {
    fn from(value: JobError) -> Self {
        Self::Job(value)
    }
}

pub struct SqliteJobStore {
    connection: Connection,
}

impl SqliteJobStore {
    pub fn open(path: impl AsRef<Path>) -> Result<Self, SqliteJobError> {
        let connection = Connection::open(path)?;
        connection.execute_batch(
            "PRAGMA foreign_keys = ON;
             PRAGMA journal_mode = WAL;
             CREATE TABLE IF NOT EXISTS jobs (
                 id TEXT PRIMARY KEY NOT NULL,
                 tenant_id TEXT NOT NULL,
                 idempotency_key TEXT NOT NULL,
                 state TEXT NOT NULL,
                 limits_json TEXT NOT NULL,
                 attempt INTEGER NOT NULL CHECK (attempt >= 1),
                 created_at_unix_ms INTEGER NOT NULL DEFAULT
                   (CAST(strftime('%s','now') AS INTEGER) * 1000),
                 UNIQUE (tenant_id, idempotency_key)
             );
             CREATE INDEX IF NOT EXISTS idx_jobs_tenant_state
                 ON jobs (tenant_id, state);",
        )?;
        Ok(Self { connection })
    }

    pub fn submit(
        &mut self,
        id: &str,
        tenant: &str,
        idempotency_key: &str,
        limits: ResourceLimits,
    ) -> Result<Job, SqliteJobError> {
        if id.trim().is_empty() || tenant.trim().is_empty() || idempotency_key.trim().is_empty() {
            return Err(JobError::EmptyIdentifier.into());
        }
        limits.validate()?;
        let limits_json = serde_json::to_string(&limits)?;
        let transaction = self.connection.transaction()?;
        let existing_id: Option<String> = transaction
            .query_row(
                "SELECT id FROM jobs WHERE tenant_id = ?1 AND idempotency_key = ?2",
                params![tenant, idempotency_key],
                |row| row.get(0),
            )
            .optional()?;
        if let Some(existing_id) = existing_id {
            let existing = load_job(&transaction, tenant, &existing_id)?;
            if existing.limits != limits {
                return Err(JobError::IdempotencyConflict.into());
            }
            transaction.commit()?;
            return Ok(existing);
        }
        transaction.execute(
            "INSERT INTO jobs (id, tenant_id, idempotency_key, state, limits_json, attempt)
             VALUES (?1, ?2, ?3, 'queued', ?4, 1)",
            params![id, tenant, idempotency_key, limits_json],
        )?;
        let job = load_job(&transaction, tenant, id)?;
        transaction.commit()?;
        Ok(job)
    }

    pub fn get(&self, tenant: &str, id: &str) -> Result<Job, SqliteJobError> {
        load_job(&self.connection, tenant, id)
    }

    pub fn transition(&mut self, tenant: &str, id: &str, next: JobState) -> Result<Job, SqliteJobError> {
        let transaction = self.connection.transaction()?;
        let current = load_job(&transaction, tenant, id)?;
        let valid = matches!(
            (&current.state, &next),
            (JobState::Queued, JobState::Running)
                | (JobState::Queued, JobState::Cancelled)
                | (JobState::Running, JobState::Succeeded)
                | (JobState::Running, JobState::Failed)
                | (JobState::Running, JobState::Cancelled)
        );
        if !valid {
            return Err(JobError::InvalidTransition.into());
        }
        transaction.execute(
            "UPDATE jobs SET state = ?1 WHERE id = ?2 AND tenant_id = ?3",
            params![state_name(&next), id, tenant],
        )?;
        let updated = load_job(&transaction, tenant, id)?;
        transaction.commit()?;
        Ok(updated)
    }

    /// Requeue a failed job while its configured retry budget remains.
    pub fn retry_failed(
        &mut self,
        tenant: &str,
        id: &str,
        max_attempts: u32,
    ) -> Result<Job, SqliteJobError> {
        if max_attempts == 0 {
            return Err(JobError::InvalidLimits.into());
        }
        let transaction = self.connection.transaction()?;
        let current = load_job(&transaction, tenant, id)?;
        if current.state != JobState::Failed || current.attempt >= max_attempts {
            return Err(JobError::InvalidTransition.into());
        }
        transaction.execute(
            "UPDATE jobs SET state = 'queued', attempt = attempt + 1
             WHERE id = ?1 AND tenant_id = ?2 AND state = 'failed'",
            params![id, tenant],
        )?;
        let updated = load_job(&transaction, tenant, id)?;
        transaction.commit()?;
        Ok(updated)
    }
}

fn state_name(state: &JobState) -> &'static str {
    match state {
        JobState::Queued => "queued",
        JobState::Running => "running",
        JobState::Succeeded => "succeeded",
        JobState::Failed => "failed",
        JobState::Cancelled => "cancelled",
    }
}

fn parse_state(value: &str) -> Result<JobState, rusqlite::Error> {
    match value {
        "queued" => Ok(JobState::Queued),
        "running" => Ok(JobState::Running),
        "succeeded" => Ok(JobState::Succeeded),
        "failed" => Ok(JobState::Failed),
        "cancelled" => Ok(JobState::Cancelled),
        _ => Err(rusqlite::Error::InvalidQuery),
    }
}

fn load_job(connection: &Connection, tenant: &str, id: &str) -> Result<Job, SqliteJobError> {
    let row: (String, String, String, String, String, u32) = connection
        .query_row(
            "SELECT id, tenant_id, idempotency_key, state, limits_json, attempt
         FROM jobs WHERE id = ?1 AND tenant_id = ?2",
            params![id, tenant],
            |row| {
                Ok((
                    row.get(0)?,
                    row.get(1)?,
                    row.get(2)?,
                    row.get(3)?,
                    row.get(4)?,
                    row.get(5)?,
                ))
            },
        )
        .optional()?
        .ok_or(JobError::NotFound)?;
    Ok(Job {
        id: row.0,
        tenant_id: row.1,
        idempotency_key: row.2,
        state: parse_state(&row.3)?,
        limits: serde_json::from_str(&row.4)?,
        attempt: row.5,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::tempdir;

    fn limits() -> ResourceLimits {
        ResourceLimits {
            max_runtime_seconds: 90,
            max_memory_bytes: 4096,
            max_cpu_millis: 750,
        }
    }

    #[test]
    fn jobs_survive_reopen_and_tenant_scoped_idempotency_is_stable() {
        let directory = tempdir().unwrap();
        let path = directory.path().join("jobs.sqlite");
        {
            let mut store = SqliteJobStore::open(&path).unwrap();
            let first = store
                .submit("job-1", "tenant-a", "request-1", limits())
                .unwrap();
            let duplicate = store
                .submit("job-2", "tenant-a", "request-1", limits())
                .unwrap();
            assert_eq!(first.id, duplicate.id);
        }
        let store = SqliteJobStore::open(&path).unwrap();
        assert_eq!(
            store.get("tenant-a", "job-1").unwrap().state,
            JobState::Queued
        );
        assert!(matches!(
            store.get("tenant-b", "job-1"),
            Err(SqliteJobError::Job(JobError::NotFound))
        ));
    }

    #[test]
    fn lifecycle_and_bounded_retry_are_persisted() {
        let directory = tempdir().unwrap();
        let mut store = SqliteJobStore::open(directory.path().join("jobs.sqlite")).unwrap();
        store
            .submit("job-2", "tenant-a", "request-2", limits())
            .unwrap();
        store
            .transition("tenant-a", "job-2", JobState::Running)
            .unwrap();
        store
            .transition("tenant-a", "job-2", JobState::Failed)
            .unwrap();
        let retried = store.retry_failed("tenant-a", "job-2", 2).unwrap();
        assert_eq!(retried.state, JobState::Queued);
        assert_eq!(retried.attempt, 2);
        store
            .transition("tenant-a", "job-2", JobState::Running)
            .unwrap();
        store
            .transition("tenant-a", "job-2", JobState::Failed)
            .unwrap();
        assert!(matches!(
            store.retry_failed("tenant-a", "job-2", 2),
            Err(SqliteJobError::Job(JobError::InvalidTransition))
        ));
    }
}
