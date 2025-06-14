resource "aws_ecs_service" "api" {
  name            = "iqas-service"
  cluster         = module.ecs_cluster.arn
  launch_type     = "FARGATE"
  desired_count   = 2
  task_definition = aws_ecs_task_definition.api.arn

  network_configuration {
    subnets         = module.vpc.private_subnets
    security_groups = [module.vpc.default_security_group_id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "api"
    container_port   = 8000
  }

  deployment_controller {
    type = "ECS"
  }

  lifecycle {
    ignore_changes = [desired_count] # so you can scale from the console/CLI
  }

  tags = { Environment = "prod", Project = "iqas" }
}
