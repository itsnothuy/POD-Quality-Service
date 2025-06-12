variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "us-east-1"
}

variable "ecr_image_tag" {
  type        = string
  description = "ECR URI with tag, e.g. 123456789012.dkr.ecr.us-east-1.amazonaws.com/iqas:dev"
}

variable "db_pass" {
  type        = string
  description = "Postgres master password"
  sensitive   = true
}

variable "minio_url" {
  type        = string
  description = "Internal MinIO endpoint"
  default     = "http://minio:9000"
}
