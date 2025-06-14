module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.21.0"

  name                 = "pod-vpc"
  cidr                 = "10.0.0.0/16"
  azs                  = ["${var.aws_region}a", "${var.aws_region}b"]

  public_subnets       = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnets      = ["10.0.11.0/24", "10.0.12.0/24"]
  database_subnets     = ["10.0.21.0/24", "10.0.22.0/24"]

  enable_nat_gateway           = true
  single_nat_gateway           = true
  create_database_subnet_group = true

  tags = { Environment = "prod", Project = "iqas" }
}
