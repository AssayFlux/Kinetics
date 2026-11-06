use std::{env, net::SocketAddr, sync::Arc};

use aws_sdk_s3::Client as S3Client;
use axum::{
    body::Bytes,
    extract::{Path, State},
    http::{header::AUTHORIZATION, HeaderMap, StatusCode},
    response::{IntoResponse, Response},
    routing::{get, post},
    Json, Router,
};
use chrono::Utc;
use serde::{Deserialize, Serialize};
use serde_json::json;
use sqlx::postgres::PgPoolOptions;
use tokio::net::TcpListener;
use tower_http::{limit::RequestBodyLimitLayer, trace::TraceLayer};
use uuid::Uuid;

use kinetics_infra::{
    cloud_artifacts::{CloudArtifactError, S3ArtifactStore},
    cloud_secrets::AwsSecretProvider,
    oidc::{AuthenticatedPrincipal, OidcError, OidcVerifier},
    postgres::{
        AppendAuditEvent, AppendOnlyAuditStore, JobSubmissionLimits, PostgresRuntimeStore,
        RuntimeStoreError,
    },
};

#[derive(Clone)]
struct AppState {
    oidc: Arc<OidcVerifier>,
    artifacts: S3ArtifactStore,
    jobs: PostgresRuntimeStore,
    audit: AppendOnlyAuditStore,
    max_runtime_seconds: i64,
    max_memory_bytes: i64,
    max_cpu_millis: i32,
    max_active_jobs: i64,
}

#[derive(Debug, Serialize)]
struct ErrorBody {
    error: &'static str,
}

#[derive(Debug)]
struct ApiError(StatusCode, &'static str);

impl IntoResponse for ApiError {
    fn into_response(self) -> Response {
        (self.0, Json(ErrorBody { error: self.1 })).into_response()
    }
}

fn database_url_from_secret(secret: &str) -> Result<String, Box<dyn std::error::Error>> {
    if secret.starts_with("postgres://") || secret.starts_with("postgresql://") {
        return Ok(secret.to_owned());
    }
    let value: serde_json::Value = serde_json::from_str(secret)?;
    let mut url = url::Url::parse("postgres://localhost/postgres")?;
    url.set_username(
        value["username"]
            .as_str()
            .ok_or("RDS secret missing username")?,
    )?;
    url.set_password(Some(
        value["password"]
            .as_str()
            .ok_or("RDS secret missing password")?,
    ))
    .map_err(|_| "invalid database password")?;
    url.set_host(Some(
        value["host"].as_str().ok_or("RDS secret missing host")?,
    ))?;
    if let Some(port) = value["port"].as_u64() {
        url.set_port(Some(port as u16))
            .map_err(|_| "invalid database port")?;
    }
    url.set_path(value["dbname"].as_str().unwrap_or("kinetics"));
    Ok(url.to_string())
}

fn env_required(name: &str) -> Result<String, Box<dyn std::error::Error>> {
    env::var(name).map_err(|_| format!("required configuration missing: {name}").into())
}

async fn principal(
    state: &AppState,
    headers: &HeaderMap,
    scope: &str,
) -> Result<AuthenticatedPrincipal, ApiError> {
    let authorization = headers
        .get(AUTHORIZATION)
        .and_then(|value| value.to_str().ok());
    let user = state
        .oidc
        .verify_authorization(authorization)
        .await
        .map_err(|error| match error {
            OidcError::MissingToken | OidcError::InvalidToken => {
                ApiError(StatusCode::UNAUTHORIZED, "unauthorized")
            }
            OidcError::Forbidden => ApiError(StatusCode::FORBIDDEN, "forbidden"),
            OidcError::ProviderUnavailable => ApiError(
                StatusCode::SERVICE_UNAVAILABLE,
                "identity_provider_unavailable",
            ),
        })?;
    user.require_scope(scope)
        .map_err(|_| ApiError(StatusCode::FORBIDDEN, "forbidden"))?;
    Ok(user)
}

async fn audit(
    state: &AppState,
    user: &AuthenticatedPrincipal,
    action: &str,
    resource_type: &str,
    resource_id: &str,
    outcome: &str,
) -> Result<(), ApiError> {
    let event = AppendAuditEvent {
        event_id: Uuid::new_v4(),
        tenant_id: user.tenant_id.clone(),
        actor_subject: user.subject.clone(),
        action: action.to_owned(),
        resource_type: resource_type.to_owned(),
        resource_id: resource_id.to_owned(),
        outcome: outcome.to_owned(),
        correlation_id: Uuid::new_v4().to_string(),
        occurred_at: Utc::now(),
    };
    state
        .audit
        .append(&event)
        .await
        .map(|_| ())
        .map_err(|_| ApiError(StatusCode::SERVICE_UNAVAILABLE, "audit_unavailable"))
}

async fn health() -> Json<serde_json::Value> {
    Json(json!({"status":"ok","api_version":"v1"}))
}

#[derive(Serialize)]
struct ArtifactReceipt {
    sha256: String,
    size_bytes: usize,
}

async fn upload_artifact(
    State(state): State<AppState>,
    headers: HeaderMap,
    body: Bytes,
) -> Result<Json<ArtifactReceipt>, ApiError> {
    let user = principal(&state, &headers, "artifacts:write").await?;
    let size_bytes = body.len();
    let digest = state
        .artifacts
        .put(&user.tenant_id, body.to_vec())
        .await
        .map_err(|error| match error {
            CloudArtifactError::TooLarge => {
                ApiError(StatusCode::PAYLOAD_TOO_LARGE, "artifact_too_large")
            }
            CloudArtifactError::Integrity => ApiError(StatusCode::BAD_REQUEST, "invalid_artifact"),
            CloudArtifactError::Storage => ApiError(
                StatusCode::SERVICE_UNAVAILABLE,
                "artifact_storage_unavailable",
            ),
        })?;
    audit(
        &state,
        &user,
        "artifact.upload",
        "artifact",
        &digest,
        "success",
    )
    .await?;
    Ok(Json(ArtifactReceipt {
        sha256: digest,
        size_bytes,
    }))
}

async fn download_artifact(
    State(state): State<AppState>,
    headers: HeaderMap,
    Path(digest): Path<String>,
) -> Result<Response, ApiError> {
    let user = principal(&state, &headers, "artifacts:read").await?;
    let bytes = state
        .artifacts
        .get(&user.tenant_id, &digest)
        .await
        .map_err(|error| match error {
            CloudArtifactError::TooLarge => {
                ApiError(StatusCode::PAYLOAD_TOO_LARGE, "artifact_too_large")
            }
            CloudArtifactError::Integrity => ApiError(
                StatusCode::INTERNAL_SERVER_ERROR,
                "artifact_integrity_failed",
            ),
            CloudArtifactError::Storage => ApiError(StatusCode::NOT_FOUND, "artifact_not_found"),
        })?;
    audit(
        &state,
        &user,
        "artifact.download",
        "artifact",
        &digest,
        "success",
    )
    .await?;
    Ok((
        [(axum::http::header::CONTENT_TYPE, "application/octet-stream")],
        bytes,
    )
        .into_response())
}

#[derive(Deserialize)]
struct SubmitJobBody {
    idempotency_key: String,
    payload: serde_json::Value,
    max_runtime_seconds: i64,
    max_memory_bytes: i64,
    max_cpu_millis: i32,
}

async fn submit_job(
    State(state): State<AppState>,
    headers: HeaderMap,
    Json(body): Json<SubmitJobBody>,
) -> Result<(StatusCode, Json<serde_json::Value>), ApiError> {
    let user = principal(&state, &headers, "jobs:write").await?;
    if body.max_runtime_seconds <= 0
        || body.max_runtime_seconds > state.max_runtime_seconds
        || body.max_memory_bytes <= 0
        || body.max_memory_bytes > state.max_memory_bytes
        || body.max_cpu_millis <= 0
        || body.max_cpu_millis > state.max_cpu_millis
    {
        return Err(ApiError(
            StatusCode::UNPROCESSABLE_ENTITY,
            "resource_limit_exceeded",
        ));
    }
    let job = state
        .jobs
        .submit(
            &user.tenant_id,
            &body.idempotency_key,
            body.payload,
            JobSubmissionLimits {
                max_runtime_seconds: body.max_runtime_seconds,
                max_memory_bytes: body.max_memory_bytes,
                max_cpu_millis: body.max_cpu_millis,
                max_active_jobs: state.max_active_jobs,
            },
        )
        .await
        .map_err(map_store_error)?;
    audit(
        &state,
        &user,
        "job.submit",
        "job",
        &job.id.to_string(),
        "success",
    )
    .await?;
    Ok((
        StatusCode::ACCEPTED,
        Json(serde_json::to_value(job).unwrap_or_else(|_| json!({}))),
    ))
}

async fn get_job(
    State(state): State<AppState>,
    headers: HeaderMap,
    Path(id): Path<Uuid>,
) -> Result<Json<serde_json::Value>, ApiError> {
    let user = principal(&state, &headers, "jobs:read").await?;
    let job = state
        .jobs
        .get(&user.tenant_id, id)
        .await
        .map_err(map_store_error)?;
    audit(&state, &user, "job.read", "job", &id.to_string(), "success").await?;
    Ok(Json(
        serde_json::to_value(job).unwrap_or_else(|_| json!({})),
    ))
}

async fn cancel_job(
    State(state): State<AppState>,
    headers: HeaderMap,
    Path(id): Path<Uuid>,
) -> Result<StatusCode, ApiError> {
    let user = principal(&state, &headers, "jobs:write").await?;
    state
        .jobs
        .request_cancel(&user.tenant_id, id)
        .await
        .map_err(map_store_error)?;
    audit(
        &state,
        &user,
        "job.cancel",
        "job",
        &id.to_string(),
        "accepted",
    )
    .await?;
    Ok(StatusCode::ACCEPTED)
}

fn map_store_error(error: RuntimeStoreError) -> ApiError {
    match error {
        RuntimeStoreError::NotFound => ApiError(StatusCode::NOT_FOUND, "not_found"),
        RuntimeStoreError::QuotaExceeded => {
            ApiError(StatusCode::TOO_MANY_REQUESTS, "tenant_job_quota_exceeded")
        }
        RuntimeStoreError::Conflict => ApiError(StatusCode::CONFLICT, "job_conflict"),
        RuntimeStoreError::Database(_) => {
            ApiError(StatusCode::SERVICE_UNAVAILABLE, "database_unavailable")
        }
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt()
        .json()
        .with_env_filter(env::var("RUST_LOG").unwrap_or_else(|_| "info,tower_http=info".into()))
        .init();

    let aws_config = aws_config::load_defaults(aws_config::BehaviorVersion::latest()).await;
    let secrets = AwsSecretProvider::from_default_identity().await;
    let (admin_url, app_url, app_password) =
        if env::var("KINETICS_ENV").as_deref() == Ok("development") {
            let url = env_required("DATABASE_URL")?;
            (url.clone(), url, None)
        } else {
            let admin_id = env_required("KINETICS_DATABASE_ADMIN_SECRET_ID")?;
            let app_id = env_required("KINETICS_DATABASE_SECRET_ID")?;
            let admin = database_url_from_secret(&secrets.get(&admin_id).await?)?;
            let app_secret = secrets.get(&app_id).await?;
            let app_json: serde_json::Value = serde_json::from_str(&app_secret)?;
            let password = app_json["password"]
                .as_str()
                .ok_or("app database secret missing password")?
                .to_owned();
            (
                admin,
                database_url_from_secret(&app_secret)?,
                Some(password),
            )
        };

    let admin_pool = PgPoolOptions::new()
        .max_connections(4)
        .connect(&admin_url)
        .await?;
    sqlx::query("SELECT pg_advisory_lock(729103)")
        .execute(&admin_pool)
        .await?;
    let migration = include_str!("../migrations/0001_runtime.sql");
    sqlx::raw_sql(migration).execute(&admin_pool).await?;
    sqlx::query("SELECT pg_advisory_unlock(729103)")
        .execute(&admin_pool)
        .await?;
    if let Some(password) = app_password {
        let escaped = password.replace('\'', "''");
        let role_exists: bool = sqlx::query_scalar(
            "SELECT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'kinetics_app')",
        )
        .fetch_one(&admin_pool)
        .await?;
        let statement = if role_exists {
            format!("ALTER ROLE kinetics_app WITH LOGIN PASSWORD '{escaped}'")
        } else {
            format!("CREATE ROLE kinetics_app LOGIN PASSWORD '{escaped}'")
        };
        sqlx::raw_sql(&statement).execute(&admin_pool).await?;
        let database_name =
            env::var("KINETICS_DATABASE_NAME").unwrap_or_else(|_| "kinetics".into());
        let quoted_database = format!("\"{}\"", database_name.replace('"', "\"\""));
        let grants = format!(
            "GRANT CONNECT ON DATABASE {quoted_database} TO kinetics_app;
             GRANT USAGE ON SCHEMA public TO kinetics_app;
             GRANT SELECT, INSERT, UPDATE ON kinetics_jobs TO kinetics_app;
             GRANT SELECT, INSERT ON kinetics_audit_events TO kinetics_app;
             GRANT USAGE, SELECT ON SEQUENCE kinetics_audit_events_sequence_id_seq TO kinetics_app;"
        );
        sqlx::raw_sql(&grants).execute(&admin_pool).await?;
    }
    admin_pool.close().await;
    let pool = PgPoolOptions::new()
        .max_connections(20)
        .connect(&app_url)
        .await?;

    let bucket = env_required("KINETICS_ARTIFACT_BUCKET")?;
    let kms_key = env_required("KINETICS_ARTIFACT_KMS_KEY_ID")?;
    let s3 = S3Client::new(&aws_config);
    let oidc = OidcVerifier::new(
        env_required("OIDC_ISSUER")?,
        env_required("OIDC_AUDIENCE")?,
        env_required("OIDC_JWKS_URL")?,
    );
    let max_artifact_bytes = env::var("KINETICS_MAX_ARTIFACT_BYTES")
        .unwrap_or_else(|_| "52428800".into())
        .parse()?;
    let state = AppState {
        oidc: Arc::new(oidc),
        artifacts: S3ArtifactStore::new(s3, bucket, kms_key, max_artifact_bytes),
        jobs: PostgresRuntimeStore::new(pool.clone()),
        audit: AppendOnlyAuditStore::new(pool),
        max_runtime_seconds: env::var("KINETICS_MAX_RUNTIME_SECONDS")
            .unwrap_or_else(|_| "86400".into())
            .parse()?,
        max_memory_bytes: env::var("KINETICS_MAX_MEMORY_BYTES")
            .unwrap_or_else(|_| "17179869184".into())
            .parse()?,
        max_cpu_millis: env::var("KINETICS_MAX_CPU_MILLIS")
            .unwrap_or_else(|_| "8000".into())
            .parse()?,
        max_active_jobs: env::var("KINETICS_MAX_ACTIVE_JOBS_PER_TENANT")
            .unwrap_or_else(|_| "20".into())
            .parse()?,
    };
    let app = Router::new()
        .route("/health", get(health))
        .route("/api/v1/artifacts", post(upload_artifact))
        .route("/api/v1/artifacts/:digest", get(download_artifact))
        .route("/api/v1/jobs", post(submit_job))
        .route("/api/v1/jobs/:id", get(get_job).delete(cancel_job))
        .with_state(state)
        .layer(RequestBodyLimitLayer::new(max_artifact_bytes))
        .layer(TraceLayer::new_for_http());

    let address: SocketAddr = env::var("KINETICS_BIND")
        .unwrap_or_else(|_| "0.0.0.0:8080".into())
        .parse()?;
    let listener = TcpListener::bind(address).await?;
    tracing::info!(%address, "Kinetics API listening");
    axum::serve(listener, app).await?;
    Ok(())
}
