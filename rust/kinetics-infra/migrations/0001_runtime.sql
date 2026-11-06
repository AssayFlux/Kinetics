CREATE TABLE IF NOT EXISTS kinetics_jobs (
    id UUID PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    payload JSONB NOT NULL,
    state TEXT NOT NULL CHECK (state IN ('queued','running','succeeded','failed','cancelled')),
    attempt INTEGER NOT NULL DEFAULT 1 CHECK (attempt > 0),
    max_attempts INTEGER NOT NULL DEFAULT 3 CHECK (max_attempts > 0),
    max_runtime_seconds BIGINT NOT NULL CHECK (max_runtime_seconds > 0),
    max_memory_bytes BIGINT NOT NULL CHECK (max_memory_bytes > 0),
    max_cpu_millis INTEGER NOT NULL CHECK (max_cpu_millis > 0),
    cancel_requested BOOLEAN NOT NULL DEFAULT FALSE,
    lease_owner TEXT,
    lease_expires_at TIMESTAMPTZ,
    next_attempt_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    started_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, idempotency_key)
);
CREATE INDEX IF NOT EXISTS kinetics_jobs_claim_idx
    ON kinetics_jobs (state, lease_expires_at, created_at)
    WHERE cancel_requested = FALSE;
CREATE INDEX IF NOT EXISTS kinetics_jobs_tenant_idx
    ON kinetics_jobs (tenant_id, created_at DESC);

CREATE TABLE IF NOT EXISTS kinetics_audit_events (
    sequence_id BIGSERIAL PRIMARY KEY,
    event_id UUID NOT NULL UNIQUE,
    tenant_id TEXT NOT NULL,
    actor_subject TEXT NOT NULL,
    action TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    resource_id TEXT NOT NULL,
    outcome TEXT NOT NULL,
    correlation_id TEXT NOT NULL,
    occurred_at TIMESTAMPTZ NOT NULL,
    previous_hash TEXT,
    event_hash TEXT NOT NULL UNIQUE
);

CREATE OR REPLACE FUNCTION kinetics_audit_immutable()
RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION 'kinetics audit events are append-only';
END;
$$;

DROP TRIGGER IF EXISTS kinetics_audit_no_update ON kinetics_audit_events;
CREATE TRIGGER kinetics_audit_no_update
    BEFORE UPDATE OR DELETE ON kinetics_audit_events
    FOR EACH ROW EXECUTE FUNCTION kinetics_audit_immutable();
