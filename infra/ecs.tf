# 1) ECS Cluster
module "ecs_cluster" {
  source  = "terraform-aws-modules/ecs/aws//modules/cluster"
  version = "5.12.1"

  cluster_name = "iqas"
  tags = {
    Environment = "prod"
    Project     = "iqas"
  }
}

# 2) Container Definition
module "api_container_def" {
  source  = "terraform-aws-modules/ecs/aws//modules/container-definition"
  version = "5.12.1"

  name       = "api"
  image      = var.ecr_image_tag
  cpu        = 512
  memory     = 1024
  essential  = true

  port_mappings = [{
    containerPort = 8000
    hostPort      = 8000
    protocol      = "tcp"
  }]

  environment = [
    {
      name  = "DATABASE_URL"
      value = module.rds.db_instance_endpoint
    },
    {
      name  = "MINIO_ENDPOINT_INTERNAL"
      value = var.minio_url
    }
  ]

  health_check = {
    command      = ["CMD-SHELL","curl -f http://localhost:8000/healthz || exit 1"]
    interval     = 30
    retries      = 3
    timeout      = 5
    start_period = 10
  }
}

# 3) ECS Service on Fargate
module "ecs_service" {
  source  = "terraform-aws-modules/ecs/aws//modules/service"
  version = "5.12.1"

  name        = "iqas-service"
  cluster_arn = module.ecs_cluster.arn

  launch_type   = "FARGATE"
  network_mode  = "awsvpc"
  desired_count = 2

  subnet_ids         = module.vpc.private_subnets
  security_group_ids = [module.vpc.default_security_group_id]

  container_definitions = {
    api = module.api_container_def.container_definition
  }

  # --- fixed ---
  load_balancer = [
    {
      target_group_arn = aws_lb_target_group.api.arn
      container_name   = "api"
      container_port   = 8000
    }
  ]
}

