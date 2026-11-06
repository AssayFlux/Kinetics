use aws_sdk_secretsmanager::Client;
use thiserror::Error;

#[derive(Debug, Error)]
pub enum ManagedSecretError {
    #[error("managed secret is unavailable")]
    Unavailable,
    #[error("managed secret has no string value")]
    InvalidValue,
}

/// AWS Secrets Manager adapter. Credentials come from the AWS SDK provider
/// chain (ECS task role, IRSA, instance profile, or local SSO), never from API input.
#[derive(Clone)]
pub struct AwsSecretProvider {
    client: Client,
}

impl AwsSecretProvider {
    pub async fn from_default_identity() -> Self {
        let config = aws_config::load_defaults(aws_config::BehaviorVersion::latest()).await;
        Self {
            client: Client::new(&config),
        }
    }

    pub async fn get(&self, secret_id: &str) -> Result<String, ManagedSecretError> {
        let output = self
            .client
            .get_secret_value()
            .secret_id(secret_id)
            .send()
            .await
            .map_err(|_| ManagedSecretError::Unavailable)?;
        output
            .secret_string()
            .map(str::to_owned)
            .ok_or(ManagedSecretError::InvalidValue)
    }
}
