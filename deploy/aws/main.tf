terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "aws" {
  region = var.region
}

data "aws_caller_identity" "current" {}

resource "random_password" "app_database" {
  length           = 48
  special          = true
  override_special = "!#$%&*()-_=+[]{}:?"
}

resource "aws_kms_key" "artifacts" {
  description             = "${var.name} artifact encryption"
  enable_key_rotation     = true
  deletion_window_in_days = 30
}

resource "aws_kms_key" "database" {
  description             = "${var.name} RDS and runtime-secret encryption"
  enable_key_rotation     = true
  deletion_window_in_days = 30
}

resource "aws_kms_key" "backup" {
  description             = "${var.name} replicated artifact backup encryption"
  enable_key_rotation     = true
  deletion_window_in_days = 30
}

resource "aws_s3_bucket" "artifacts" {
  bucket        = "${var.name}-artifacts-${data.aws_caller_identity.current.account_id}"
  force_destroy = false
}

resource "aws_s3_bucket_versioning" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.artifacts.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "artifacts" {
  bucket                  = aws_s3_bucket.artifacts.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket" "artifact_backup" {
  bucket        = "${var.name}-artifact-backup-${data.aws_caller_identity.current.account_id}"
  force_destroy = false
}

resource "aws_s3_bucket_versioning" "artifact_backup" {
  bucket = aws_s3_bucket.artifact_backup.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "artifact_backup" {
  bucket = aws_s3_bucket.artifact_backup.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.backup.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "artifact_backup" {
  bucket                  = aws_s3_bucket.artifact_backup.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_iam_role" "artifact_replication" {
  name = "${var.name}-artifact-replication"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "s3.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "artifact_replication" {
  role = aws_iam_role.artifact_replication.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetReplicationConfiguration", "s3:ListBucket"]
        Resource = aws_s3_bucket.artifacts.arn
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObjectVersionForReplication",
          "s3:GetObjectVersionAcl",
          "s3:GetObjectVersionTagging"
        ]
        Resource = "${aws_s3_bucket.artifacts.arn}/tenants/*"
      },
      {
        Effect   = "Allow"
        Action   = ["s3:ReplicateObject", "s3:ReplicateDelete", "s3:ReplicateTags"]
        Resource = "${aws_s3_bucket.artifact_backup.arn}/*"
      },
      {
        Effect   = "Allow"
        Action   = ["kms:Decrypt"]
        Resource = aws_kms_key.artifacts.arn
      },
      {
        Effect   = "Allow"
        Action   = ["kms:Encrypt", "kms:GenerateDataKey"]
        Resource = aws_kms_key.backup.arn
      }
    ]
  })
}

resource "aws_s3_bucket_replication_configuration" "artifacts" {
  depends_on = [
    aws_s3_bucket_versioning.artifacts,
    aws_s3_bucket_versioning.artifact_backup,
    aws_iam_role_policy.artifact_replication
  ]
  role   = aws_iam_role.artifact_replication.arn
  bucket = aws_s3_bucket.artifacts.id

  rule {
    id     = "replicate-tenant-artifacts"
    status = "Enabled"
    filter {
      prefix = "tenants/"
    }
    source_selection_criteria {
      sse_kms_encrypted_objects {
        status = "Enabled"
      }
    }
    destination {
      bucket        = aws_s3_bucket.artifact_backup.arn
      storage_class = "STANDARD"
      encryption_configuration {
        replica_kms_key_id = aws_kms_key.backup.arn
      }
    }
    delete_marker_replication {
      status = "Disabled"
    }
  }
}

resource "aws_s3_bucket_policy" "artifacts_tls" {
  bucket     = aws_s3_bucket.artifacts.id
  depends_on = [aws_s3_bucket_public_access_block.artifacts]
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "DenyInsecureTransport"
      Effect    = "Deny"
      Principal = "*"
      Action    = "s3:*"
      Resource  = [aws_s3_bucket.artifacts.arn, "${aws_s3_bucket.artifacts.arn}/*"]
      Condition = { Bool = { "aws:SecureTransport" = "false" } }
    }]
  })
}

resource "aws_db_subnet_group" "database" {
  name       = "${var.name}-db"
  subnet_ids = var.private_subnet_ids
}

resource "aws_security_group" "database" {
  name        = "${var.name}-database"
  description = "PostgreSQL accepts traffic only from Kinetics tasks"
  vpc_id      = var.vpc_id
}

resource "aws_security_group" "tasks" {
  name        = "${var.name}-tasks"
  description = "Kinetics ECS task network policy"
  vpc_id      = var.vpc_id
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group_rule" "database_from_tasks" {
  type                     = "ingress"
  security_group_id        = aws_security_group.database.id
  source_security_group_id = aws_security_group.tasks.id
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
}

resource "aws_db_instance" "database" {
  identifier                    = "${var.name}-postgres"
  engine                        = "postgres"
  engine_version                = "16"
  instance_class                = "db.t4g.medium"
  allocated_storage             = 100
  max_allocated_storage         = 500
  storage_encrypted             = true
  kms_key_id                    = aws_kms_key.database.arn
  db_name                       = var.database_name
  username                      = var.database_username
  manage_master_user_password   = true
  master_user_secret_kms_key_id = aws_kms_key.database.arn
  db_subnet_group_name          = aws_db_subnet_group.database.name
  vpc_security_group_ids        = [aws_security_group.database.id]
  publicly_accessible           = false
  multi_az                      = true
  backup_retention_period       = 14
  deletion_protection           = true
  skip_final_snapshot           = false
  final_snapshot_identifier     = "${var.name}-final-snapshot"
  auto_minor_version_upgrade    = true
  copy_tags_to_snapshot         = true
}

resource "aws_secretsmanager_secret" "app_database" {
  name       = "${var.name}/database/runtime"
  kms_key_id = aws_kms_key.database.arn
}

resource "aws_secretsmanager_secret_version" "app_database" {
  secret_id = aws_secretsmanager_secret.app_database.id
  secret_string = jsonencode({
    username = var.app_database_username
    password = random_password.app_database.result
    host     = aws_db_instance.database.address
    port     = aws_db_instance.database.port
    dbname   = var.database_name
  })
  depends_on = [aws_db_instance.database]
}

resource "aws_cloudwatch_log_group" "api" {
  name              = "/ecs/${var.name}/api"
  retention_in_days = 90
}

resource "aws_cloudwatch_log_group" "worker" {
  name              = "/ecs/${var.name}/worker"
  retention_in_days = 90
}

resource "aws_iam_role" "execution" {
  name = "${var.name}-ecs-execution"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "execution" {
  role       = aws_iam_role.execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role" "api_task" {
  name               = "${var.name}-api-task"
  assume_role_policy = aws_iam_role.execution.assume_role_policy
}

resource "aws_iam_role_policy" "api_task" {
  role = aws_iam_role.api_task.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:PutObject"]
        Resource = "${aws_s3_bucket.artifacts.arn}/tenants/*"
      },
      {
        Effect   = "Allow"
        Action   = ["kms:Encrypt", "kms:Decrypt", "kms:GenerateDataKey", "kms:DescribeKey"]
        Resource = aws_kms_key.artifacts.arn
      },
      {
        Effect = "Allow"
        Action = ["secretsmanager:GetSecretValue"]
        Resource = [
          aws_db_instance.database.master_user_secret[0].secret_arn,
          aws_secretsmanager_secret.app_database.arn
        ]
      },
      {
        Effect   = "Allow"
        Action   = ["kms:Decrypt"]
        Resource = aws_kms_key.database.arn
      }
    ]
  })
}

resource "aws_iam_role" "worker_task" {
  name = "${var.name}-worker-task"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "worker_task" {
  role = aws_iam_role.worker_task.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["secretsmanager:GetSecretValue"]
        Resource = aws_secretsmanager_secret.app_database.arn
      },
      {
        Effect   = "Allow"
        Action   = ["kms:Decrypt"]
        Resource = aws_kms_key.database.arn
      }
    ]
  })
}

resource "aws_ecs_cluster" "main" {
  name = var.name
}

resource "aws_ecs_task_definition" "api" {
  family                   = "${var.name}-api"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "1024"
  memory                   = "2048"
  execution_role_arn       = aws_iam_role.execution.arn
  task_role_arn            = aws_iam_role.api_task.arn
  container_definitions = jsonencode([{
    name      = "api"
    image     = var.image_uri
    essential = true
    portMappings = [{
      containerPort = 8080
      protocol      = "tcp"
    }]
    environment = [
      { name = "KINETICS_ENV", value = "production" },
      { name = "KINETICS_BIND", value = "0.0.0.0:8080" },
      { name = "KINETICS_ARTIFACT_BUCKET", value = aws_s3_bucket.artifacts.bucket },
      { name = "KINETICS_ARTIFACT_KMS_KEY_ID", value = aws_kms_key.artifacts.arn },
      { name = "KINETICS_DATABASE_ADMIN_SECRET_ID", value = aws_db_instance.database.master_user_secret[0].secret_arn },
      { name = "KINETICS_DATABASE_SECRET_ID", value = aws_secretsmanager_secret.app_database.arn },
      { name = "KINETICS_DATABASE_NAME", value = var.database_name },
      { name = "OIDC_ISSUER", value = var.oidc_issuer },
      { name = "OIDC_AUDIENCE", value = var.oidc_audience },
      { name = "OIDC_JWKS_URL", value = var.oidc_jwks_url },
      { name = "KINETICS_MAX_ACTIVE_JOBS_PER_TENANT", value = "20" },
      { name = "KINETICS_MAX_ARTIFACT_BYTES", value = "52428800" },
      { name = "KINETICS_MAX_CPU_MILLIS", value = "4000" },
      { name = "KINETICS_MAX_MEMORY_BYTES", value = "8589934592" }
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = aws_cloudwatch_log_group.api.name
        awslogs-region        = var.region
        awslogs-stream-prefix = "api"
      }
    }
    healthCheck = {
      command     = ["CMD-SHELL", "curl -fsS http://127.0.0.1:8080/health || exit 1"]
      interval    = 30
      timeout     = 5
      retries     = 3
      startPeriod = 30
    }
  }])
}

resource "aws_ecs_task_definition" "worker" {
  family                   = "${var.name}-worker"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "4096"
  memory                   = "8192"
  execution_role_arn       = aws_iam_role.execution.arn
  task_role_arn            = aws_iam_role.worker_task.arn
  container_definitions = jsonencode([{
    name       = "worker"
    image      = var.image_uri
    essential  = true
    entryPoint = ["/usr/local/bin/kinetics-worker"]
    environment = [
      { name = "KINETICS_DATABASE_SECRET_ID", value = aws_secretsmanager_secret.app_database.arn },
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = aws_cloudwatch_log_group.worker.name
        awslogs-region        = var.region
        awslogs-stream-prefix = "worker"
      }
    }
  }])
}

resource "aws_security_group" "alb" {
  name   = "${var.name}-alb"
  vpc_id = var.vpc_id
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = var.allowed_api_cidrs
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = var.allowed_api_cidrs
  }
  egress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.tasks.id]
  }
}

resource "aws_security_group_rule" "api_from_alb" {
  type                     = "ingress"
  security_group_id        = aws_security_group.tasks.id
  source_security_group_id = aws_security_group.alb.id
  from_port                = 8080
  to_port                  = 8080
  protocol                 = "tcp"
}

resource "aws_lb" "api" {
  name               = "${var.name}-api"
  internal           = false
  load_balancer_type = "application"
  subnets            = var.public_subnet_ids
  security_groups    = [aws_security_group.alb.id]
}

resource "aws_lb_target_group" "api" {
  name        = "${var.name}-api"
  port        = 8080
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"
  health_check {
    path    = "/health"
    matcher = "200"
  }
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.api.arn
  port              = 443
  protocol          = "HTTPS"
  certificate_arn   = var.certificate_arn
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.api.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type = "redirect"
    redirect {
      port        = "443"
      protocol    = "HTTPS"
      status_code = "HTTP_301"
    }
  }
}

resource "aws_ecs_service" "api" {
  name            = "${var.name}-api"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = var.api_desired_count
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.tasks.id]
    assign_public_ip = false
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "api"
    container_port   = 8080
  }
  depends_on = [aws_lb_listener.https]
}

resource "aws_ecs_service" "worker" {
  name            = "${var.name}-worker"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.worker.arn
  desired_count   = var.worker_desired_count
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.tasks.id]
    assign_public_ip = false
  }
}
