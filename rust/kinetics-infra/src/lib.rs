//! Small, auditable infrastructure primitives. Production deployments must
//! provide durable databases, an external identity provider, and managed keys.
pub mod artifacts;
pub mod audit;
pub mod auth;
pub mod jobs;

pub const API_VERSION: &str = "v1";
