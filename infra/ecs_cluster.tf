module "ecs_cluster" {
  source  = "terraform-aws-modules/ecs/aws//modules/cluster"
  version = "5.12.1"

  cluster_name = "iqas"
  tags         = { Environment = "prod", Project = "iqas" }
}
