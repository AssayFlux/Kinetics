output "api_url" {
  value = "https://${aws_lb.api.dns_name}"
}

output "database_secret_arn" {
  value     = aws_db_instance.database.master_user_secret[0].secret_arn
  sensitive = true
}

output "artifact_bucket" {
  value = aws_s3_bucket.artifacts.bucket
}

output "kms_key_arn" {
  value = aws_kms_key.artifacts.arn
}
