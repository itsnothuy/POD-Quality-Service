terraform {
  required_version = ">=1.7"
  backend "s3" {
    bucket = "pod-tf-state2"          # ← create this bucket once
    key    = "infra/terraform.tfstate"
    region = "us-east-1"
  }
  required_providers { 
    aws    = { source = "hashicorp/aws",    version = ">= 5.99.1" }
    random = { source = "hashicorp/random", version = ">= 3.7.2" }
  }
}

provider "aws" {
  region = var.aws_region
}
