use kinetics_infra::secrets::{SecretError, SecretString};

#[test]
fn blank_secret_name_is_rejected_without_reading_environment() {
    assert_eq!(SecretString::from_env("  ").err(), Some(SecretError::InvalidName));
}
