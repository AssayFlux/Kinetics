use std::collections::BTreeSet;

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Principal {
    pub subject: String,
    pub tenant_id: String,
    scopes: BTreeSet<String>,
}

impl Principal {
    pub fn new(subject: impl Into<String>, tenant_id: impl Into<String>,
               scopes: impl IntoIterator<Item = String>) -> Result<Self, AuthError> {
        let subject = subject.into();
        let tenant_id = tenant_id.into();
        if subject.trim().is_empty() || tenant_id.trim().is_empty() {
            return Err(AuthError::InvalidPrincipal);
        }
        Ok(Self { subject, tenant_id, scopes: scopes.into_iter().collect() })
    }

    pub fn require_scope(&self, required: &str) -> Result<(), AuthError> {
        if self.scopes.contains(required) { Ok(()) } else { Err(AuthError::Forbidden) }
    }

    pub fn require_tenant(&self, tenant_id: &str) -> Result<(), AuthError> {
        if self.tenant_id == tenant_id { Ok(()) } else { Err(AuthError::NotFound) }
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum AuthError { InvalidPrincipal, Forbidden, NotFound }

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn scopes_and_tenant_boundaries_are_enforced() {
        let user = Principal::new("alice", "tenant-a", ["artifact:read".to_string()]).unwrap();
        assert!(user.require_scope("artifact:read").is_ok());
        assert_eq!(user.require_scope("job:admin"), Err(AuthError::Forbidden));
        assert_eq!(user.require_tenant("tenant-b"), Err(AuthError::NotFound));
    }
}
