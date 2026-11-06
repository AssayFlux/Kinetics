use sha2::{Digest, Sha256};
use std::{
    fs, io,
    path::{Path, PathBuf},
};

#[derive(Debug)]
pub enum ArtifactError {
    Io(io::Error),
    InvalidDigest,
    IntegrityMismatch,
}

impl From<io::Error> for ArtifactError {
    fn from(value: io::Error) -> Self {
        Self::Io(value)
    }
}

pub fn sha256_hex(bytes: &[u8]) -> String {
    let digest = Sha256::digest(bytes);
    digest.iter().map(|byte| format!("{byte:02x}")).collect()
}

pub struct ArtifactStore {
    root: PathBuf,
}

impl ArtifactStore {
    pub fn new(root: impl AsRef<Path>) -> Result<Self, ArtifactError> {
        fs::create_dir_all(root.as_ref())?;
        Ok(Self {
            root: root.as_ref().to_path_buf(),
        })
    }

    fn object_path(&self, digest: &str) -> Result<PathBuf, ArtifactError> {
        if digest.len() != 64
            || !digest
                .bytes()
                .all(|b| b.is_ascii_hexdigit() && !b.is_ascii_uppercase())
        {
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
        match fs::OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(&path)
        {
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
        if sha256_hex(&bytes) != digest {
            return Err(ArtifactError::IntegrityMismatch);
        }
        Ok(bytes)
    }

    pub fn verify(&self, digest: &str) -> Result<(), ArtifactError> {
        self.get(digest).map(|_| ())
    }

    /// Copy every verified object into a separate content-addressed backup.
    pub fn backup_to(&self, destination: impl AsRef<Path>) -> Result<(), ArtifactError> {
        let backup = ArtifactStore::new(destination)?;
        backup.import_verified_objects(&self.root)
    }

    /// Restore verified objects from a backup. Existing identical objects are
    /// idempotent; corrupt objects and unexpected filesystem entries are rejected.
    pub fn restore_from(&self, source: impl AsRef<Path>) -> Result<(), ArtifactError> {
        self.import_verified_objects(source.as_ref())
    }

    fn import_verified_objects(&self, source: &Path) -> Result<(), ArtifactError> {
        for prefix_entry in fs::read_dir(source)? {
            let prefix_entry = prefix_entry?;
            if !prefix_entry.file_type()?.is_dir() {
                return Err(ArtifactError::InvalidDigest);
            }
            let prefix = prefix_entry.file_name().to_string_lossy().into_owned();
            if prefix.len() != 2
                || !prefix.bytes().all(|byte| byte.is_ascii_hexdigit() && !byte.is_ascii_uppercase())
            {
                return Err(ArtifactError::InvalidDigest);
            }
            for object_entry in fs::read_dir(prefix_entry.path())? {
                let object_entry = object_entry?;
                if !object_entry.file_type()?.is_file() {
                    return Err(ArtifactError::InvalidDigest);
                }
                let digest = object_entry.file_name().to_string_lossy().into_owned();
                if !digest.starts_with(&prefix) {
                    return Err(ArtifactError::InvalidDigest);
                }
                let bytes = fs::read(object_entry.path())?;
                if sha256_hex(&bytes) != digest {
                    return Err(ArtifactError::IntegrityMismatch);
                }
                self.put(&bytes)?;
            }
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn backup_restore_preserves_objects_and_rejects_tampering() {
        let directory = tempfile::tempdir().unwrap();
        let source = ArtifactStore::new(directory.path().join("source")).unwrap();
        let backup_path = directory.path().join("backup");
        let restored = ArtifactStore::new(directory.path().join("restored")).unwrap();
        let digest = source.put(b"recovery fixture").unwrap();
        source.backup_to(&backup_path).unwrap();
        restored.restore_from(&backup_path).unwrap();
        assert_eq!(restored.get(&digest).unwrap(), b"recovery fixture");

        let object_path = backup_path.join(&digest[..2]).join(&digest);
        fs::write(&object_path, b"tampered").unwrap();
        assert!(matches!(
            restored.restore_from(&backup_path),
            Err(ArtifactError::IntegrityMismatch)
        ));
    }

    #[test]
    fn content_addressed_round_trip_and_path_traversal_rejection() {
        let dir = tempfile::tempdir().unwrap();
        let store = ArtifactStore::new(dir.path()).unwrap();
        let hash = store.put(b"scientific artifact").unwrap();
        assert_eq!(store.get(&hash).unwrap(), b"scientific artifact");
        assert!(matches!(
            store.get("../etc/passwd"),
            Err(ArtifactError::InvalidDigest)
        ));
    }
}
