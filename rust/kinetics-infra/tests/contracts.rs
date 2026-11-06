use kinetics_infra::{audit::AuditEvent, API_VERSION};

#[test]
fn api_version_and_audit_contract_are_serializable() {
    assert_eq!(API_VERSION, "v1");
    let event = AuditEvent {
        event_id: "evt-1".into(),
        occurred_at_unix_ms: 1,
        actor_subject: "researcher-1".into(),
        tenant_id: "lab-1".into(),
        action: "artifact.read".into(),
        resource_type: "artifact".into(),
        resource_id: "sha256:abc".into(),
        outcome: "success".into(),
        correlation_id: "request-1".into(),
    };
    event.validate().unwrap();
    let json = serde_json::to_string(&event).unwrap();
    assert!(json.contains("\"tenant_id\":\"lab-1\""));
}
