data "aws_iam_policy_document" "task_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "task" {
  name               = "iqas-task-role"
  assume_role_policy = data.aws_iam_policy_document.task_assume.json
}

# add any extra IAM policies your container needs here
# resource "aws_iam_role_policy_attachment" ...

resource "aws_iam_role" "task_execution" {
  name               = "iqas-task-exec-role"
  assume_role_policy = data.aws_iam_policy_document.task_assume.json
}

resource "aws_iam_role_policy_attachment" "task_exec_default" {
  role       = aws_iam_role.task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

locals {
  container_def = [
    {
      name      = "api"
      image     = var.ecr_image_tag
      cpu       = 512
      memory    = 1024
      essential = true

      portMappings = [
        {
          name          = "api-8000"
          containerPort = 8000
          hostPort      = 8000
          protocol      = "tcp"
        }
      ]

      environment = [
        { name = "DATABASE_URL",            value = module.rds.db_instance_endpoint },
        { name = "MINIO_ENDPOINT_INTERNAL", value = var.minio_url                   }
      ]

      healthCheck = {
        command     = ["CMD-SHELL", "curl -f http://localhost:8000/healthz || exit 1"]
        interval    = 30
        retries     = 3
        timeout     = 5
        startPeriod = 10
      }

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/aws/ecs/iqas-service/api"
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ]
}


resource "aws_ecs_task_definition" "api" {
  family                   = "iqas-service"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"

  execution_role_arn = aws_iam_role.task_execution.arn
  task_role_arn      = aws_iam_role.task.arn

  container_definitions = jsonencode(local.container_def)
}
