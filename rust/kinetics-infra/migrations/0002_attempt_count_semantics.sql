-- Attempt counts represent actual worker claims, not an unstarted queued row.
-- Normalize pre-existing queued jobs that have never been claimed before changing
-- the default, preserving attempt counts for running and previously retried jobs.
UPDATE kinetics_jobs
SET attempt = 0
WHERE state = 'queued' AND started_at IS NULL;

ALTER TABLE kinetics_jobs
    ALTER COLUMN attempt SET DEFAULT 0;

ALTER TABLE kinetics_jobs
    DROP CONSTRAINT IF EXISTS kinetics_jobs_attempt_check;

ALTER TABLE kinetics_jobs
    ADD CONSTRAINT kinetics_jobs_attempt_check CHECK (attempt >= 0);
