use aws_sdk_s3::{primitives::ByteStream, types::ServerSideEncryption, Client};
use sha2::{Digest, Sha256};
use thiserror::Error;

#[derive(Debug, Error)]
pub enum CloudArtifactError {
    #[error("artifact storage operation failed")]
    Storage,
    #[error("artifact content integrity check failed")]
    Integrity,
    #[error("artifact exceeds configured size limit")]
    TooLarge,
}

#[derive(Clone)]
pub struct S3ArtifactStore {
    client: Client,
    bucket: String,
    kms_key_id: String,
    max_bytes: usize,
}

impl S3ArtifactStore {
    pub fn new(client: Client, bucket: String, kms_key_id: String, max_bytes: usize) -> Self {
        Self {
            client,
            bucket,
            kms_key_id,
            max_bytes,
        }
    }

    fn tenant_prefix(tenant_id: &str) -> String {
        let digest = Sha256::digest(tenant_id.as_bytes());
        digest.iter().map(|byte| format!("{byte:02x}")).collect()
    }

    fn digest(bytes: &[u8]) -> String {
        let digest = Sha256::digest(bytes);
        digest.iter().map(|byte| format!("{byte:02x}")).collect()
    }

    fn key(tenant_id: &str, digest: &str) -> String {
        format!(
            "tenants/{}/artifacts/{}/{}",
            Self::tenant_prefix(tenant_id),
            &digest[..2],
            digest
        )
    }

    pub async fn put(&self, tenant_id: &str, bytes: Vec<u8>) -> Result<String, CloudArtifactError> {
        if bytes.len() > self.max_bytes {
            return Err(CloudArtifactError::TooLarge);
        }
        let digest = Self::digest(&bytes);
        self.client
            .put_object()
            .bucket(&self.bucket)
            .key(Self::key(tenant_id, &digest))
            .body(ByteStream::from(bytes))
            .server_side_encryption(ServerSideEncryption::AwsKms)
            .ssekms_key_id(&self.kms_key_id)
            .metadata("sha256", digest.clone())
            .send()
            .await
            .map_err(|_| CloudArtifactError::Storage)?;
        Ok(digest)
    }

    pub async fn get(&self, tenant_id: &str, digest: &str) -> Result<Vec<u8>, CloudArtifactError> {
        if digest.len() != 64
            || !digest
                .bytes()
                .all(|b| b.is_ascii_hexdigit() && !b.is_ascii_uppercase())
        {
            return Err(CloudArtifactError::Integrity);
        }
        let output = self
            .client
            .get_object()
            .bucket(&self.bucket)
            .key(Self::key(tenant_id, digest))
            .send()
            .await
            .map_err(|_| CloudArtifactError::Storage)?;
        let bytes = output
            .body
            .collect()
            .await
            .map_err(|_| CloudArtifactError::Storage)?
            .into_bytes()
            .to_vec();
        if bytes.len() > self.max_bytes || Self::digest(&bytes) != digest {
            return Err(CloudArtifactError::Integrity);
        }
        Ok(bytes)
    }
}

#[cfg(test)]
mod tenant_key_tests {
    use super::*;

    #[test]
    fn tenant_prefix_is_one_way_and_isolates_identical_artifact_digests() {
        let a = S3ArtifactStore::tenant_prefix("tenant-alpha");
        let b = S3ArtifactStore::tenant_prefix("tenant-beta");
        assert_ne!(a, b);
        assert!(!a.contains("tenant-alpha"));
        let digest = "a".repeat(64);
        assert_ne!(
            S3ArtifactStore::key("tenant-alpha", &digest),
            S3ArtifactStore::key("tenant-beta", &digest)
        );
    }
}
