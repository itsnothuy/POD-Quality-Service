module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "6.12.0"

  identifier             = "pod-db"
  engine                 = "postgres"
  engine_version         = "16.9"
  instance_class         = "db.t4g.micro"
  allocated_storage      = 20
  max_allocated_storage  = 100

  db_name                = "iqas"            # renamed from deprecated `name`
  username               = "iqas"
  password               = var.db_pass

  # supply the required family for the parameter-group submodule
  family                 = "postgres16"

  subnet_ids             = module.vpc.private_subnets
  depends_on = [aws_security_group.rds]

  publicly_accessible    = false
  skip_final_snapshot    = true
}
