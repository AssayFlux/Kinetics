//! Small, auditable infrastructure primitives. Production deployments must
//! provide durable databases, an external identity provider, and managed keys.
pub mod artifacts;
pub mod audit;
pub mod auth;
pub mod contracts;
pub mod cloud_artifacts;
pub mod cloud_secrets;
pub mod jobs;
pub mod oidc;
pub mod postgres;
pub mod secrets;
pub mod sqlite_jobs;
pub mod worker;

pub const API_VERSION: &str = "v1";
