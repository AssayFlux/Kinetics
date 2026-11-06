use sha2::{Digest, Sha256};
use std::{fs, io, path::{Path, PathBuf}};

#[derive(Debug)]
pub enum ArtifactError { Io(io::Error), InvalidDigest, IntegrityMismatch }
impl From<io::Error> for ArtifactError { fn from(value: io::Error) -> Self { Self::Io(value) } }

pub fn sha256_hex(bytes: &[u8]) -> String {
    let digest = Sha256::digest(bytes);
    digest.iter().map(|byte| format!("{byte:02x}")).collect()
}

pub struct ArtifactStore { root: PathBuf }

impl ArtifactStore {
    pub fn new(root: impl AsRef<Path>) -> Result<Self, ArtifactError> {
        fs::create_dir_all(root.as_ref())?;
        Ok(Self { root: root.as_ref().to_path_buf() })
    }

    fn object_path(&self, digest: &str) -> Result<PathBuf, ArtifactError> {
        if digest.len() != 64 || !digest.bytes().all(|b| b.is_ascii_hexdigit() && !b.is_ascii_uppercase()) {
            return Err(ArtifactError::InvalidDigest);
        }
        Ok(self.root.join(&digest[..2]).join(digest))
    }

    /// Content-addressed, immutable write. A digest is the only accepted key;
    /// user-supplied filenames are never interpreted as filesystem paths.
    pub fn put(&self, bytes: &[u8]) -> Result<String, ArtifactError> {
        let digest = sha256_hex(bytes);
        let path = self.object_path(&digest)?;
        if path.exists() {
            self.verify(&digest)?;
            return Ok(digest);
        }
        let parent = path.parent().ok_or(ArtifactError::InvalidDigest)?;
        fs::create_dir_all(parent)?;
        match fs::OpenOptions::new().write(true).create_new(true).open(&path) {
            Ok(mut file) => {
                use std::io::Write;
                file.write_all(bytes)?;
                file.sync_all()?;
            }
            Err(error) if error.kind() == io::ErrorKind::AlreadyExists => {
                self.verify(&digest)?;
            }
            Err(error) => return Err(ArtifactError::Io(error)),
        }
        Ok(digest)
    }

    pub fn get(&self, digest: &str) -> Result<Vec<u8>, ArtifactError> {
        let bytes = fs::read(self.object_path(digest)?)?;
        if sha256_hex(&bytes) != digest { return Err(ArtifactError::IntegrityMismatch); }
        Ok(bytes)
    }

    pub fn verify(&self, digest: &str) -> Result<(), ArtifactError> {
        self.get(digest).map(|_| ())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn content_addressed_round_trip_and_path_traversal_rejection() {
        let dir = tempfile::tempdir().unwrap();
        let store = ArtifactStore::new(dir.path()).unwrap();
        let hash = store.put(b"scientific artifact").unwrap();
        assert_eq!(store.get(&hash).unwrap(), b"scientific artifact");
        assert!(matches!(store.get("../etc/passwd"), Err(ArtifactError::InvalidDigest)));
    }
}
