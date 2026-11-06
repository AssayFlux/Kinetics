variable "name" {
  type    = string
  default = "kinetics"
}

variable "region" {
  type    = string
  default = "ap-south-1"
}

variable "vpc_id" {
  type = string
}

variable "public_subnet_ids" {
  type = list(string)
}

variable "private_subnet_ids" {
  type = list(string)
}

variable "certificate_arn" {
  type        = string
  description = "ACM certificate ARN for the public API hostname"
}

variable "image_uri" {
  type        = string
  description = "Immutable ECR image URI including tag or digest"
}

variable "oidc_issuer" {
  type = string
}

variable "oidc_audience" {
  type = string
}

variable "oidc_jwks_url" {
  type = string
}

variable "database_name" {
  type    = string
  default = "kinetics"
}

variable "database_username" {
  type    = string
  default = "kinetics_admin"
}

variable "app_database_username" {
  type    = string
  default = "kinetics_app"
}

variable "api_desired_count" {
  type    = number
  default = 2
}

variable "worker_desired_count" {
  type    = number
  default = 2
}

variable "allowed_api_cidrs" {
  type        = list(string)
  description = "Explicit source CIDR allowlist for the public API; no open default is provided."
}
