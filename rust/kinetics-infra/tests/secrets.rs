use kinetics_infra::secrets::SecretString;

#[test]
fn secret_debug_is_redacted() {
    let secret = SecretString::from_env("KINETICS_TEST_SECRET")
        .unwrap_or_else(|_| panic!("test secret should be supplied by the test process"));
    assert!(!format!("{secret:?}").contains("test-secret-value"));
}
