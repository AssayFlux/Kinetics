use serde::{Deserialize, Serialize};

use crate::jobs::{Job, ResourceLimits};

pub const OPENAPI_VERSION: &str = "3.1.0";

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct SubmitJobRequest {
    pub idempotency_key: String,
    pub resource_limits: ResourceLimits,
}

impl SubmitJobRequest {
    pub fn validate(&self) -> Result<(), ContractError> {
        if self.idempotency_key.trim().is_empty() || self.idempotency_key.len() > 200 {
            return Err(ContractError::InvalidIdempotencyKey);
        }
        self.resource_limits
            .validate()
            .map_err(|_| ContractError::InvalidResourceLimits)
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct JobResponse {
    pub api_version: String,
    pub job: Job,
}

impl JobResponse {
    pub fn new(job: Job) -> Self {
        Self {
            api_version: crate::API_VERSION.to_string(),
            job,
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ArtifactResponse {
    pub api_version: String,
    pub sha256: String,
    pub size_bytes: u64,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ApiError {
    pub api_version: String,
    pub code: String,
    pub message: String,
    pub correlation_id: String,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum ContractError {
    InvalidIdempotencyKey,
    InvalidResourceLimits,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn request_contract_rejects_empty_keys_and_unbounded_resources() {
        let request = SubmitJobRequest {
            idempotency_key: " ".into(),
            resource_limits: ResourceLimits {
                max_runtime_seconds: 1,
                max_memory_bytes: 1,
                max_cpu_millis: 1,
            },
        };
        assert_eq!(
            request.validate(),
            Err(ContractError::InvalidIdempotencyKey)
        );
    }
}
