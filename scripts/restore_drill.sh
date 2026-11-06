#!/usr/bin/env bash
set -euo pipefail

: "${KINETICS_BACKUP_BUCKET:?Set the versioned, KMS-encrypted backup bucket}"
: "${KINETICS_RESTORE_DATABASE_URL:?Set an isolated, disposable PostgreSQL restore target}"
: "${KINETICS_BACKUP_KEY:?Set the exact backup object key to restore}"

workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT
aws s3 cp "s3://${KINETICS_BACKUP_BUCKET}/${KINETICS_BACKUP_KEY}" "$workdir/kinetics.dump"
aws s3 cp "s3://${KINETICS_BACKUP_BUCKET}/${KINETICS_BACKUP_KEY}.sha256" "$workdir/kinetics.dump.sha256"
(cd "$workdir" && sha256sum --check kinetics.dump.sha256)
pg_restore --clean --if-exists --no-owner --no-acl --dbname "$KINETICS_RESTORE_DATABASE_URL" "$workdir/kinetics.dump"
psql "$KINETICS_RESTORE_DATABASE_URL" -v ON_ERROR_STOP=1 -c "SELECT count(*) AS restored_jobs FROM kinetics_jobs;"
psql "$KINETICS_RESTORE_DATABASE_URL" -v ON_ERROR_STOP=1 -c "SELECT count(*) AS restored_audit_events FROM kinetics_audit_events;"
echo "Restore drill completed. Review row counts and application-level integrity before signing off."
