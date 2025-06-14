
module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "6.12.0"

  identifier            = "pod-db"
  engine                = "postgres"
  engine_version        = "16.9"
  instance_class        = "db.t4g.micro"

  allocated_storage     = 20
  max_allocated_storage = 100

  db_name   = "iqas"
  username  = "iqas"
  password  = var.db_pass
  family    = "postgres16"

  db_subnet_group_name   = module.vpc.database_subnet_group
  vpc_security_group_ids = [aws_security_group.rds.id]

  publicly_accessible = false
  skip_final_snapshot = true
}
