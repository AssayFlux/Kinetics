use std::collections::HashMap;

use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum JobState {
    Queued,
    Running,
    Succeeded,
    Failed,
    Cancelled,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ResourceLimits {
    pub max_runtime_seconds: u64,
    pub max_memory_bytes: u64,
    pub max_cpu_millis: u32,
}

impl ResourceLimits {
    pub fn validate(&self) -> Result<(), JobError> {
        if self.max_runtime_seconds == 0
            || self.max_memory_bytes == 0
            || self.max_cpu_millis == 0
        {
            return Err(JobError::InvalidLimits);
        }
        Ok(())
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Job {
    pub id: String,
    pub tenant_id: String,
    pub idempotency_key: String,
    pub state: JobState,
    pub limits: ResourceLimits,
    pub attempt: u32,
}

#[derive(Default)]
pub struct JobRegistry {
    jobs: HashMap<String, Job>,
    idempotency: HashMap<(String, String), String>,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum JobError {
    InvalidLimits,
    EmptyIdentifier,
    IdempotencyConflict,
    NotFound,
    InvalidTransition,
}

impl JobRegistry {
    pub fn submit(
        &mut self,
        id: &str,
        tenant: &str,
        key: &str,
        limits: ResourceLimits,
    ) -> Result<Job, JobError> {
        if id.trim().is_empty() || tenant.trim().is_empty() || key.trim().is_empty() {
            return Err(JobError::EmptyIdentifier);
        }
        limits.validate()?;
        let idem = (tenant.to_string(), key.to_string());
        if let Some(existing_id) = self.idempotency.get(&idem) {
            let existing = self.jobs.get(existing_id).ok_or(JobError::NotFound)?;
            if existing.limits != limits {
                return Err(JobError::IdempotencyConflict);
            }
            return Ok(existing.clone());
        }
        if self.jobs.contains_key(id) {
            return Err(JobError::IdempotencyConflict);
        }
        let job = Job {
            id: id.to_string(),
            tenant_id: tenant.to_string(),
            idempotency_key: key.to_string(),
            state: JobState::Queued,
            limits,
            attempt: 1,
        };
        self.idempotency.insert(idem, id.to_string());
        self.jobs.insert(id.to_string(), job.clone());
        Ok(job)
    }

    pub fn transition(
        &mut self,
        tenant: &str,
        id: &str,
        next: JobState,
    ) -> Result<Job, JobError> {
        let job = self.jobs.get_mut(id).ok_or(JobError::NotFound)?;
        if job.tenant_id != tenant {
            return Err(JobError::NotFound);
        }
        let valid = matches!(
            (&job.state, &next),
            (JobState::Queued, JobState::Running)
                | (JobState::Queued, JobState::Cancelled)
                | (JobState::Running, JobState::Succeeded)
                | (JobState::Running, JobState::Failed)
                | (JobState::Running, JobState::Cancelled)
        );
        if !valid {
            return Err(JobError::InvalidTransition);
        }
        job.state = next;
        Ok(job.clone())
    }

    pub fn get(&self, tenant: &str, id: &str) -> Result<Job, JobError> {
        let job = self.jobs.get(id).ok_or(JobError::NotFound)?;
        if job.tenant_id != tenant {
            return Err(JobError::NotFound);
        }
        Ok(job.clone())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn limits() -> ResourceLimits {
        ResourceLimits {
            max_runtime_seconds: 60,
            max_memory_bytes: 1024,
            max_cpu_millis: 500,
        }
    }

    #[test]
    fn idempotency_is_tenant_scoped_and_conflicts_are_rejected() {
        let mut registry = JobRegistry::default();
        let first = registry.submit("j1", "a", "same", limits()).unwrap();
        let repeat = registry.submit("j2", "a", "same", limits()).unwrap();
        assert_eq!(first.id, repeat.id);
        assert_eq!(
            registry.submit(
                "j3",
                "a",
                "same",
                ResourceLimits {
                    max_runtime_seconds: 1,
                    ..limits()
                }
            ),
            Err(JobError::IdempotencyConflict)
        );
        assert_ne!(
            registry.submit("j4", "b", "same", limits()).unwrap().id,
            first.id
        );
    }

    #[test]
    fn lifecycle_and_cross_tenant_reads_are_restricted() {
        let mut registry = JobRegistry::default();
        registry.submit("j1", "a", "k", limits()).unwrap();
        assert_eq!(registry.get("b", "j1"), Err(JobError::NotFound));
        registry.transition("a", "j1", JobState::Running).unwrap();
        registry.transition("a", "j1", JobState::Cancelled).unwrap();
        assert_eq!(
            registry.transition("a", "j1", JobState::Succeeded),
            Err(JobError::InvalidTransition)
        );
    }

    #[test]
    fn zero_resource_limits_are_rejected() {
        let mut registry = JobRegistry::default();
        assert_eq!(
            registry.submit(
                "j",
                "a",
                "k",
                ResourceLimits {
                    max_runtime_seconds: 0,
                    ..limits()
                }
            ),
            Err(JobError::InvalidLimits)
        );
    }
}
