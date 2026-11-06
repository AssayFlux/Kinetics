#!/usr/bin/env bash
set -euo pipefail
umask 077

: "${KINETICS_DATABASE_URL:?Set the runtime PostgreSQL URL from the secret manager}"
: "${KINETICS_BACKUP_BUCKET:?Set the encrypted backup bucket}"
: "${KINETICS_BACKUP_KMS_KEY_ID:?Set the backup KMS key ARN}"

workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"; unset PGPASSWORD' EXIT
export KINETICS_BACKUP_STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
export KINETICS_BACKUP_KEY="postgres/${KINETICS_BACKUP_STAMP}/kinetics.dump"

eval "$(python3 - <<'PY'
import os
from urllib.parse import unquote, urlparse
url = urlparse(os.environ["KINETICS_DATABASE_URL"])
if url.scheme not in {"postgres", "postgresql"} or not url.hostname:
    raise SystemExit("invalid PostgreSQL connection URL")
values = {
    "PGHOST": url.hostname,
    "PGPORT": str(url.port or 5432),
    "PGUSER": unquote(url.username or ""),
    "PGPASSWORD": unquote(url.password or ""),
    "PGDATABASE": (url.path or "/").lstrip("/"),
    "PGSSLMODE": "require",
}
for key, value in values.items():
    print(f"export {key}={value!r}")
PY
)"

pg_dump --no-password --format=custom --no-owner --no-acl --file "$workdir/kinetics.dump"
sha256sum "$workdir/kinetics.dump" > "$workdir/kinetics.dump.sha256"
aws s3 cp "$workdir/kinetics.dump" "s3://${KINETICS_BACKUP_BUCKET}/${KINETICS_BACKUP_KEY}" \
  --sse aws:kms --sse-kms-key-id "$KINETICS_BACKUP_KMS_KEY_ID"
aws s3 cp "$workdir/kinetics.dump.sha256" "s3://${KINETICS_BACKUP_BUCKET}/${KINETICS_BACKUP_KEY}.sha256" \
  --sse aws:kms --sse-kms-key-id "$KINETICS_BACKUP_KMS_KEY_ID"
echo "Encrypted PostgreSQL backup uploaded: ${KINETICS_BACKUP_KEY}"
