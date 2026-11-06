use std::{env, fmt};

/// A runtime-injected secret whose Debug representation never exposes its value.
/// Production deployments should source secrets from a managed secret provider.
pub struct SecretString(String);

impl SecretString {
    pub fn from_env(name: &str) -> Result<Self, SecretError> {
        if name.trim().is_empty() {
            return Err(SecretError::InvalidName);
        }
        let value = env::var(name).map_err(|_| SecretError::Unavailable)?;
        if value.is_empty() {
            return Err(SecretError::Unavailable);
        }
        Ok(Self(value))
    }

    pub fn expose_to_authorized_client(&self) -> &str {
        &self.0
    }
}

impl fmt::Debug for SecretString {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        formatter.write_str("SecretString([REDACTED])")
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum SecretError {
    InvalidName,
    Unavailable,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn debug_output_never_contains_secret_value() {
        let secret = SecretString("sensitive-value".to_string());
        let rendered = format!("{secret:?}");
        assert!(!rendered.contains("sensitive-value"));
        assert!(rendered.contains("REDACTED"));
    }

    #[test]
    fn blank_environment_variable_names_are_rejected() {
        assert_eq!(
            SecretString::from_env("  ").err(),
            Some(SecretError::InvalidName)
        );
    }
}
