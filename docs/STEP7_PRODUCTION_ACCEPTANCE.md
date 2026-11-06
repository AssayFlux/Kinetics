# Step 7 production acceptance and security review

## Runtime architecture implemented in this branch

- Identity: RS256 JWT verification against an HTTPS OIDC JWKS endpoint; issuer, audience, expiry, key ID, subject, tenant claim and exact scopes are checked. JWKS keys are cached for five minutes and provider failures fail closed.
- Secrets: AWS Secrets Manager adapter uses the AWS SDK default workload identity chain. The ECS API task can read the RDS administrator bootstrap secret and a separate generated runtime credential. The worker can read only the runtime credential. No static AWS access keys are configured.
- HTTP API: Axum v1 API exposes health, tenant-bound artifact upload/download, job submission/read/cancellation. Authorization is checked per route. Tenant identity comes only from verified claims; callers cannot submit a tenant identifier. Request body and artifact size are bounded.
- Artifacts: S3 object keys use a one-way tenant namespace and SHA-256 content digest. Uploads and downloads verify content hashes. S3 enforces KMS encryption, versioning, TLS-only bucket policy, public-access blocking, and replication to a separately encrypted versioned backup bucket.
- Jobs: PostgreSQL stores durable jobs, tenant-scoped idempotency, admission quotas, state, bounded attempts, lease owner and expiry. Multiple workers claim with row-level SKIP LOCKED semantics; expired leases are reclaimed, heartbeats extend leases, runtime deadlines are applied, and cancellation is propagated.
- Resource envelope: API admission caps jobs at the deployment's configured maximum. ECS Fargate worker tasks are separately capped at 4 vCPU and 8 GiB and run one job at a time. The per-request values are admission metadata and runtime timeout; strict per-job CPU/memory isolation requires the scientific executor to run as a separately provisioned Fargate task or a cgroup-enforced sandbox. Do not represent the current shared worker task envelope as per-job cgroup enforcement.
- Audit: Events are serialized in a single PostgreSQL transaction under an advisory lock and chained by SHA-256. Database trigger rejects update/delete. The API uses a runtime DB role granted SELECT/INSERT only on audit events; the migration administrator is separate.
- Database: RDS PostgreSQL is private, Multi-AZ, encrypted with KMS, and configured with 14-day automated backups and deletion protection. The API bootstraps schema and the least-privilege runtime DB role from Secrets Manager; workers never receive the administrator secret.
- Recovery: S3 artifact replication is encrypted with a separate KMS key. scripts/backup_postgres.sh creates a custom-format database dump and uploads it with KMS encryption and a SHA-256 sidecar. scripts/restore_drill.sh verifies and restores a selected backup into an isolated PostgreSQL target.

## Production configuration

Terraform under deploy/aws requires an existing VPC with public and private subnets, an ACM certificate, an immutable ECR image URI, and the OIDC issuer/audience/JWKS URL. Private subnets need outbound access through NAT or VPC endpoints for ECR, CloudWatch, Secrets Manager, KMS, S3, and the OIDC JWKS endpoint.

The application accepts only RS256 access tokens. The identity provider must issue tenant_id and space-delimited scope claims for the configured API audience. Required scopes are artifacts:read, artifacts:write, jobs:read, and jobs:write.

The Terraform state contains generated application database credentials and must be stored in an encrypted, access-controlled remote backend with state locking. Do not commit terraform.tfstate, plan files, secret values, or tfvars containing credentials.

## Deployment sequence

1. Build and publish the Docker image to ECR; use an immutable digest for image_uri.
2. Supply VPC/subnet IDs, ACM certificate ARN and OIDC values in a protected tfvars file or CI environment.
3. Run terraform init, terraform plan, and have an authorized operator review IAM, networking, RDS cost and data residency before terraform apply.
4. Verify the ALB certificate and HTTPS redirect, health checks, task logs, RDS connectivity and JWKS reachability.
5. Test access tokens for valid signature, wrong issuer, wrong audience, expiry, missing tenant claim and missing scopes.
6. Test tenant A upload/read and tenant B denial for the same digest; test job get/cancel IDOR and quota boundaries.
7. Run the PostgreSQL integration suite against a disposable database and verify audit update/delete denial.
8. Run a database backup, restore it to an isolated target, compare row counts and application-level checks, then retain the signed drill report.
9. Verify an artifact appears in the backup bucket with KMS encryption and object versioning; perform an isolated restore and SHA-256 verification.
10. Review AWS Config/Security Hub findings, IAM Access Analyzer, container image scan, dependency audit, secret scan, log retention and incident response contacts before production traffic.

## Explicit acceptance limits

This repository change supplies deployable code and infrastructure definitions. It does not create cloud resources, register an OIDC application, publish an image, apply Terraform, or perform a live disaster-recovery drill. The production worker currently has an allow-listed health-check task only; the Kinetics scientific task handlers must be registered before accepting scientific workloads. Per-job CPU/memory isolation must be moved to one Fargate task per job (or an equivalent cgroup sandbox) before multi-tenant untrusted workloads are enabled.

The live deployment, provider-specific claim mapping, cloud IAM review, real artifact restore, database restore, penetration testing, and scientific executor integration are release gates—not inferred from passing CI.
