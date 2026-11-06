use std::{
    sync::Arc,
    time::{Duration, Instant},
};

use jsonwebtoken::{
    decode, decode_header, jwk::JwkSet, Algorithm, DecodingKey, TokenData, Validation,
};
use serde::Deserialize;
use thiserror::Error;
use tokio::sync::RwLock;

#[derive(Clone, Debug, Deserialize)]
pub struct VerifiedClaims {
    pub sub: String,
    pub iss: String,
    pub aud: Audience,
    pub exp: usize,
    pub tenant_id: String,
    #[serde(default)]
    pub scope: String,
}

#[derive(Clone, Debug, Deserialize)]
#[serde(untagged)]
pub enum Audience {
    One(String),
    Many(Vec<String>),
}

#[derive(Clone, Debug)]
pub struct AuthenticatedPrincipal {
    pub subject: String,
    pub tenant_id: String,
    scopes: Vec<String>,
}

impl AuthenticatedPrincipal {
    pub fn require_scope(&self, required: &str) -> Result<(), OidcError> {
        if self.scopes.iter().any(|scope| scope == required) {
            Ok(())
        } else {
            Err(OidcError::Forbidden)
        }
    }
}

#[derive(Debug, Error)]
pub enum OidcError {
    #[error("missing or malformed bearer token")]
    MissingToken,
    #[error("token verification failed")]
    InvalidToken,
    #[error("insufficient scope")]
    Forbidden,
    #[error("identity provider unavailable")]
    ProviderUnavailable,
}

struct CachedKeys {
    loaded_at: Instant,
    keys: JwkSet,
}

#[derive(Clone)]
pub struct OidcVerifier {
    issuer: String,
    audience: String,
    jwks_url: String,
    http: reqwest::Client,
    cache: Arc<RwLock<Option<CachedKeys>>>,
}

impl OidcVerifier {
    pub fn new(issuer: String, audience: String, jwks_url: String) -> Self {
        Self {
            issuer,
            audience,
            jwks_url,
            http: reqwest::Client::builder()
                .timeout(Duration::from_secs(5))
                .https_only(true)
                .build()
                .expect("valid HTTP client configuration"),
            cache: Arc::new(RwLock::new(None)),
        }
    }

    async fn keys(&self) -> Result<JwkSet, OidcError> {
        if let Some(cached) = self.cache.read().await.as_ref() {
            if cached.loaded_at.elapsed() < Duration::from_secs(300) {
                return Ok(cached.keys.clone());
            }
        }
        let response = self
            .http
            .get(&self.jwks_url)
            .send()
            .await
            .map_err(|_| OidcError::ProviderUnavailable)?;
        if !response.status().is_success() {
            return Err(OidcError::ProviderUnavailable);
        }
        let keys = response
            .json::<JwkSet>()
            .await
            .map_err(|_| OidcError::ProviderUnavailable)?;
        *self.cache.write().await = Some(CachedKeys {
            loaded_at: Instant::now(),
            keys: keys.clone(),
        });
        Ok(keys)
    }

    pub async fn verify_authorization(
        &self,
        authorization: Option<&str>,
    ) -> Result<AuthenticatedPrincipal, OidcError> {
        let token = authorization
            .and_then(|value| value.strip_prefix("Bearer "))
            .filter(|value| !value.is_empty())
            .ok_or(OidcError::MissingToken)?;
        let header = decode_header(token).map_err(|_| OidcError::InvalidToken)?;
        if header.alg != Algorithm::RS256 {
            return Err(OidcError::InvalidToken);
        }
        let kid = header.kid.ok_or(OidcError::InvalidToken)?;
        let keys = self.keys().await?;
        let jwk = keys
            .keys
            .iter()
            .find(|key| key.common.key_id.as_deref() == Some(&kid))
            .ok_or(OidcError::InvalidToken)?;
        let decoding_key = DecodingKey::from_jwk(jwk).map_err(|_| OidcError::InvalidToken)?;
        let mut validation = Validation::new(Algorithm::RS256);
        validation.set_issuer(&[self.issuer.as_str()]);
        validation.set_audience(&[self.audience.as_str()]);
        validation.validate_exp = true;
        let data: TokenData<VerifiedClaims> =
            decode(token, &decoding_key, &validation).map_err(|_| OidcError::InvalidToken)?;
        if data.claims.sub.trim().is_empty()
            || data.claims.tenant_id.trim().is_empty()
            || data.claims.iss != self.issuer
        {
            return Err(OidcError::InvalidToken);
        }
        let scopes = data
            .claims
            .scope
            .split_whitespace()
            .map(str::to_owned)
            .collect();
        Ok(AuthenticatedPrincipal {
            subject: data.claims.sub,
            tenant_id: data.claims.tenant_id,
            scopes,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn scopes_are_exact_and_default_deny() {
        let principal = AuthenticatedPrincipal {
            subject: "u1".into(),
            tenant_id: "t1".into(),
            scopes: vec!["artifacts:read".into()],
        };
        assert!(principal.require_scope("artifacts:read").is_ok());
        assert!(matches!(
            principal.require_scope("artifacts:write"),
            Err(OidcError::Forbidden)
        ));
    }

    #[test]
    fn audience_supports_string_or_array_claims() {
        let one: Audience = serde_json::from_str("\"kinetics-api\"").unwrap();
        let many: Audience = serde_json::from_str("[\"kinetics-api\",\"other\"]").unwrap();
        assert!(matches!(one, Audience::One(_)));
        assert!(matches!(many, Audience::Many(_)));
    }
}
