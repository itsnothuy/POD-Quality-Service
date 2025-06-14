resource "aws_lb" "api" {
  name               = "pod-alb"
  load_balancer_type = "application"

  subnets         = module.vpc.public_subnets
  security_groups = [module.vpc.default_security_group_id]

  idle_timeout               = 60
  enable_http2               = true
  enable_deletion_protection = true

  tags = { Environment = "prod", Project = "iqas" }
}

resource "aws_lb_target_group" "api" {
  name        = "pod-api-tg"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = module.vpc.vpc_id
  target_type = "ip"

  health_check {
    path                = "/healthz"
    matcher             = "200-399"
    interval            = 30
    healthy_threshold   = 3
    unhealthy_threshold = 3
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.api.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }
}
