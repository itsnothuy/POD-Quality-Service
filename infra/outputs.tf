output "alb_dns" {
  description = "ALB DNS name"
  value       = aws_lb.api.dns_name
}

output "rds_endpoint" {
  description = "RDS endpoint"
  value       = module.rds.db_instance_endpoint
}

output "cluster_arn" {
  description = "ECS Cluster ARN"
  value       = module.ecs_cluster.arn
}

