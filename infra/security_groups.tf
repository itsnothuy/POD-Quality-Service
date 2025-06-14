resource "aws_security_group" "rds" {
  name_prefix = "pod-rds-"
  vpc_id      = module.vpc.vpc_id
  description = "Postgres ingress from VPC"

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Environment = "prod"
    Project     = "iqas"
  }
}
