use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct AuditEvent {
    pub event_id: String,
    pub occurred_at_unix_ms: u64,
    pub actor_subject: String,
    pub tenant_id: String,
    pub action: String,
    pub resource_type: String,
    pub resource_id: String,
    pub outcome: String,
    pub correlation_id: String,
}

impl AuditEvent {
    /// Reject fields commonly used to smuggle credentials or payloads into logs.
    pub fn validate(&self) -> Result<(), &'static str> {
        let fields = [&self.event_id, &self.actor_subject, &self.tenant_id,
            &self.action, &self.resource_type, &self.resource_id,
            &self.outcome, &self.correlation_id];
        if fields.iter().any(|field| field.trim().is_empty()) {
            return Err("audit identity and action fields must be non-empty");
        }
        if fields.iter().any(|field| {
            let lower = field.to_ascii_lowercase();
            lower.contains("bearer ") || lower.contains("token=") ||
            lower.contains("password=") || lower.contains("secret=")
        }) {
            return Err("audit fields must not contain credential-like values");
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn event(action: &str) -> AuditEvent {
        AuditEvent { event_id: "e1".into(), occurred_at_unix_ms: 1,
            actor_subject: "u1".into(), tenant_id: "t1".into(),
            action: action.into(), resource_type: "job".into(),
            resource_id: "j1".into(), outcome: "success".into(),
            correlation_id: "c1".into() }
    }
    #[test]
    fn audit_event_rejects_credential_material() {
        assert!(event("job.read").validate().is_ok());
        assert!(event("token=do-not-log").validate().is_err());
    }
}
