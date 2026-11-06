use chrono::Utc;
use kinetics_infra::postgres::{
    AppendAuditEvent, AppendOnlyAuditStore, JobSubmissionLimits, PostgresRuntimeStore, RuntimeStoreError,
};
use sqlx::{postgres::PgPoolOptions, PgPool};
use uuid::Uuid;

async fn isolated_database() -> Option<(PgPool, String)> {
    let admin_url = std::env::var("KINETICS_TEST_DATABASE_URL").ok()?;
    let mut admin = PgPool::connect(&admin_url).await.ok()?;
    let database = format!("kinetics_test_{}", Uuid::new_v4().simple());
    sqlx::query(&format!("CREATE DATABASE \"{database}\""))
        .execute(&admin)
        .await
        .ok()?;
    let mut url = url::Url::parse(&admin_url).ok()?;
    url.set_path(&database);
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(url.as_str())
        .await
        .ok()?;
    sqlx::raw_sql(include_str!("../migrations/0001_runtime.sql"))
        .execute(&pool)
        .await
        .ok()?;
    Some((pool, database))
}

async fn drop_database(pool: PgPool, database: &str, admin_url: &str) {
    pool.close().await;
    if let Ok(admin) = PgPool::connect(admin_url).await {
        let _ = sqlx::query(&format!(
            "DROP DATABASE IF EXISTS \"{database}\" WITH (FORCE)"
        ))
        .execute(&admin)
        .await;
        admin.close().await;
    }
}

#[tokio::test]
async fn postgres_enforces_tenant_quotas_leases_cancellation_and_append_only_audit() {
    let Some(admin_url) = std::env::var("KINETICS_TEST_DATABASE_URL").ok() else {
        eprintln!("Skipping PostgreSQL integration test: KINETICS_TEST_DATABASE_URL not set");
        return;
    };
    let Some((pool, database)) = isolated_database().await else {
        panic!("PostgreSQL integration database could not be created");
    };
    let jobs = PostgresRuntimeStore::new(pool.clone());
    let payload = serde_json::json!({"task":"kinetics.noop_healthcheck"});
    let limits = JobSubmissionLimits {
        max_runtime_seconds: 60,
        max_memory_bytes: 1024,
        max_cpu_millis: 500,
        max_active_jobs: 1,
    };
    let job = jobs
        .submit("tenant-a", "key-1", payload.clone(), limits)
        .await
        .unwrap();
    let repeated = jobs
        .submit("tenant-a", "key-1", payload.clone(), limits)
        .await
        .unwrap();
    assert_eq!(job.id, repeated.id);
    assert!(matches!(
        jobs.submit("tenant-a", "key-2", payload.clone(), limits)
            .await,
        Err(RuntimeStoreError::QuotaExceeded)
    ));
    assert!(matches!(
        jobs.submit(
            "tenant-a",
            "key-1",
            serde_json::json!({"task":"changed"}),
            limits
        )
        .await,
        Err(RuntimeStoreError::Conflict)
    ));
    let other_tenant = jobs
        .submit("tenant-b", "key-1", payload.clone(), limits)
        .await
        .unwrap();
    assert_ne!(job.id, other_tenant.id);
    assert!(matches!(
        jobs.get("tenant-b", job.id).await,
        Err(RuntimeStoreError::NotFound)
    ));

    let claimed = jobs.claim("worker-a", 30).await.unwrap().unwrap();
    assert_eq!(claimed.id, job.id);
    assert!(jobs.heartbeat(job.id, "worker-a", 30).await.unwrap());
    jobs.request_cancel("tenant-a", job.id).await.unwrap();
    assert!(!jobs.heartbeat(job.id, "worker-a", 30).await.unwrap());
    assert!(jobs
        .cancellation_requested(job.id, "worker-a")
        .await
        .unwrap());
    jobs.finish_cancelled(job.id, "worker-a").await.unwrap();
    assert_eq!(
        jobs.get("tenant-a", job.id).await.unwrap().state,
        "cancelled"
    );

    let audit = AppendOnlyAuditStore::new(pool.clone());
    let event = AppendAuditEvent {
        event_id: Uuid::new_v4(),
        tenant_id: "tenant-a".into(),
        actor_subject: "subject-1".into(),
        action: "job.cancel".into(),
        resource_type: "job".into(),
        resource_id: job.id.to_string(),
        outcome: "accepted".into(),
        correlation_id: Uuid::new_v4().to_string(),
        occurred_at: Utc::now(),
    };
    let first_hash = audit.append(&event).await.unwrap();
    let mut next = event.clone();
    next.event_id = Uuid::new_v4();
    next.action = "artifact.upload".into();
    let second_hash = audit.append(&next).await.unwrap();
    assert_ne!(first_hash, second_hash);
    assert!(
        sqlx::query("UPDATE kinetics_audit_events SET outcome='tampered' WHERE event_id=$1")
            .bind(event.event_id)
            .execute(&pool)
            .await
            .is_err()
    );
    assert!(
        sqlx::query("DELETE FROM kinetics_audit_events WHERE event_id=$1")
            .bind(event.event_id)
            .execute(&pool)
            .await
            .is_err()
    );

    drop_database(pool, &database, &admin_url).await;
}
