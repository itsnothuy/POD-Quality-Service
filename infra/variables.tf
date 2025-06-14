variable "aws_region" {
  description = "Region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "ecr_image_tag" {
  description = "Full ECR image URI incl. tag"
  type        = string
}

variable "db_pass" {
  description = "RDS Postgres master password"
  type        = string
  sensitive   = true
}

variable "minio_url" {
  description = "Internal URL the API uses to reach MinIO"
  type        = string
  default     = "http://minio:9000"
}
