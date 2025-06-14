output "alb_dns" {
  description = "ALB DNS name"
  value       = aws_lb.api.dns_name
}

output "rds_endpoint" {
  description = "PostgreSQL endpoint"
  value       = module.rds.db_instance_endpoint
}

output "ecs_cluster_arn" {
  description = "ECS cluster ARN"
  value       = module.ecs_cluster.arn
}
