# ============================================================================
# Risk It For The Biscuit - Enterprise AWS Infrastructure
# ============================================================================
# This Terraform configuration deploys a production-ready, scalable
# microservices architecture on AWS with high availability and security.
# ============================================================================

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Uncomment for remote state management
  # backend "s3" {
  #   bucket         = "customer-portal-terraform-state"
  #   key            = "production/terraform.tfstate"
  #   region         = "us-west-2"
  #   encrypt        = true
  #   dynamodb_table = "terraform-lock"
  # }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
      Owner       = var.owner
    }
  }
}

# ============================================================================
# DATA SOURCES
# ============================================================================

# Get available AZs
data "aws_availability_zones" "available" {
  state = "available"
  filter {
    name   = "opt-in-status"
    values = ["opt-in-not-required"]
  }
}

# Latest Amazon Linux 2 AMI for ECS
data "aws_ami" "ecs_optimized" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-ecs-hvm-*-x86_64-ebs"]
  }
}

# ==============================================================================
# VPC Module ********************************************************************
# ==============================================================================

module "vpc" {
  source = "./modules/vpc"

  project_name        = var.project_name
  environment         = var.environment
  vpc_cidr            = var.vpc_cidr
  availability_zones  = slice(data.aws_availability_zones.available.names, 0, var.az_count)
  enable_nat_gateway  = var.enable_nat_gateway
  single_nat_gateway  = var.single_nat_gateway
}

# ==============================================================================
# Security Module ***************************************************************
# ==============================================================================

module "security_groups" {
  source = "./modules/security"

  project_name = var.project_name
  environment  = var.environment
  vpc_id       = module.vpc.vpc_id
  vpc_cidr     = var.vpc_cidr
}

# ==============================================================================
# RDS Module ********************************************************************
# ==============================================================================

module "database" {
  source = "./modules/rds"

  project_name           = var.project_name
  environment            = var.environment
  vpc_id                 = module.vpc.vpc_id
  database_subnet_ids    = module.vpc.database_subnet_ids
  db_security_group_id   = module.security_groups.db_security_group_id
  
  db_instance_class      = var.db_instance_class
  db_allocated_storage   = var.db_allocated_storage
  db_engine_version      = var.db_engine_version
  db_name                = var.db_name
  db_username            = var.db_username
  db_password            = var.db_password
  
  multi_az               = var.db_multi_az
  backup_retention_period = var.db_backup_retention
  skip_final_snapshot    = var.environment != "production"
}

# ==============================================================================
# ALB Module ********************************************************************
# ==============================================================================

module "alb" {
  source = "./modules/alb"

  project_name         = var.project_name
  environment          = var.environment
  vpc_id               = module.vpc.vpc_id
  public_subnet_ids    = module.vpc.public_subnet_ids
  alb_security_group_id = module.security_groups.alb_security_group_id
  
  enable_https         = var.enable_https
  certificate_arn      = var.certificate_arn
}

# ==============================================================================
# ECS Cluster *******************************************************************
# ==============================================================================

resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }

  tags = {
    Name = "${var.project_name}-${var.environment}-cluster"
  }
}

resource "aws_ecs_cluster_capacity_providers" "main" {
  cluster_name = aws_ecs_cluster.main.name

  capacity_providers = ["FARGATE", "FARGATE_SPOT"]

  default_capacity_provider_strategy {
    capacity_provider = var.use_fargate_spot ? "FARGATE_SPOT" : "FARGATE"
    weight           = 100
    base             = 0
  }
}

# ==============================================================================
# ECS Services ******************************************************************
# ==============================================================================

# API Gateway Service
module "gateway_service" {
  source = "./modules/ecs-service"

  project_name          = var.project_name
  environment           = var.environment
  service_name          = "gateway"
  aws_region            = var.aws_region
  
  ecs_cluster_id        = aws_ecs_cluster.main.id
  ecs_cluster_name      = aws_ecs_cluster.main.name
  vpc_id                = module.vpc.vpc_id
  private_subnet_ids    = module.vpc.private_subnet_ids
  ecs_security_group_id = module.security_groups.ecs_security_group_id
  
  container_image       = "${var.ecr_repository_url}/gateway:${var.app_version}"
  container_port        = 8000
  container_cpu         = 256
  container_memory      = 512
  desired_count         = var.gateway_desired_count
  
  target_group_arn      = module.alb.gateway_target_group_arn
  
  environment_variables = {
    ENVIRONMENT = var.environment
  }
}

# Order Service
module "order_service" {
  source = "./modules/ecs-service"

  project_name          = var.project_name
  environment           = var.environment
  service_name          = "order"
  aws_region            = var.aws_region
  
  ecs_cluster_id        = aws_ecs_cluster.main.id
  ecs_cluster_name      = aws_ecs_cluster.main.name
  vpc_id                = module.vpc.vpc_id
  private_subnet_ids    = module.vpc.private_subnet_ids
  ecs_security_group_id = module.security_groups.ecs_security_group_id
  
  container_image       = "${var.ecr_repository_url}/order:${var.app_version}"
  container_port        = 8001
  container_cpu         = 512
  container_memory      = 1024
  desired_count         = var.services_desired_count
  
  environment_variables = {
    DATABASE_URL = module.database.connection_string
    ENVIRONMENT  = var.environment
  }
}

# Chatbot Service
module "chatbot_service" {
  source = "./modules/ecs-service"

  project_name          = var.project_name
  environment           = var.environment
  service_name          = "chatbot"
  aws_region            = var.aws_region
  
  ecs_cluster_id        = aws_ecs_cluster.main.id
  ecs_cluster_name      = aws_ecs_cluster.main.name
  vpc_id                = module.vpc.vpc_id
  private_subnet_ids    = module.vpc.private_subnet_ids
  ecs_security_group_id = module.security_groups.ecs_security_group_id
  
  container_image       = "${var.ecr_repository_url}/chatbot:${var.app_version}"
  container_port        = 8005
  container_cpu         = 1024
  container_memory      = 2048
  desired_count         = var.services_desired_count
  
  environment_variables = {
    OPENAI_API_KEY = var.openai_api_key
    ENVIRONMENT    = var.environment
  }
}

# Inventory Service
module "inventory_service" {
  source = "./modules/ecs-service"

  project_name          = var.project_name
  environment           = var.environment
  service_name          = "inventory"
  aws_region            = var.aws_region
  
  ecs_cluster_id        = aws_ecs_cluster.main.id
  ecs_cluster_name      = aws_ecs_cluster.main.name
  vpc_id                = module.vpc.vpc_id
  private_subnet_ids    = module.vpc.private_subnet_ids
  ecs_security_group_id = module.security_groups.ecs_security_group_id
  
  container_image       = "${var.ecr_repository_url}/inventory:${var.app_version}"
  container_port        = 8003
  container_cpu         = 512
  container_memory      = 1024
  desired_count         = var.services_desired_count
  
  environment_variables = {
    DATABASE_URL = module.database.connection_string
    ENVIRONMENT  = var.environment
  }
}

# Customer Service
module "customer_service" {
  source = "./modules/ecs-service"

  project_name          = var.project_name
  environment           = var.environment
  service_name          = "customer"
  aws_region            = var.aws_region
  
  ecs_cluster_id        = aws_ecs_cluster.main.id
  ecs_cluster_name      = aws_ecs_cluster.main.name
  vpc_id                = module.vpc.vpc_id
  private_subnet_ids    = module.vpc.private_subnet_ids
  ecs_security_group_id = module.security_groups.ecs_security_group_id
  
  container_image       = "${var.ecr_repository_url}/customer:${var.app_version}"
  container_port        = 8002
  container_cpu         = 512
  container_memory      = 1024
  desired_count         = var.services_desired_count
  
  environment_variables = {
    DATABASE_URL = module.database.connection_string
    ENVIRONMENT  = var.environment
  }
}

# Returns Service
module "returns_service" {
  source = "./modules/ecs-service"

  project_name          = var.project_name
  environment           = var.environment
  service_name          = "returns"
  aws_region            = var.aws_region
  
  ecs_cluster_id        = aws_ecs_cluster.main.id
  ecs_cluster_name      = aws_ecs_cluster.main.name
  vpc_id                = module.vpc.vpc_id
  private_subnet_ids    = module.vpc.private_subnet_ids
  ecs_security_group_id = module.security_groups.ecs_security_group_id
  
  container_image       = "${var.ecr_repository_url}/returns:${var.app_version}"
  container_port        = 8004
  container_cpu         = 512
  container_memory      = 1024
  desired_count         = var.services_desired_count
  
  environment_variables = {
    DATABASE_URL = module.database.connection_string
    ENVIRONMENT  = var.environment
  }
}

# Notification Service
module "notification_service" {
  source = "./modules/ecs-service"

  project_name          = var.project_name
  environment           = var.environment
  service_name          = "notification"
  aws_region            = var.aws_region
  
  ecs_cluster_id        = aws_ecs_cluster.main.id
  ecs_cluster_name      = aws_ecs_cluster.main.name
  vpc_id                = module.vpc.vpc_id
  private_subnet_ids    = module.vpc.private_subnet_ids
  ecs_security_group_id = module.security_groups.ecs_security_group_id
  
  container_image       = "${var.ecr_repository_url}/notification:${var.app_version}"
  container_port        = 8006
  container_cpu         = 256
  container_memory      = 512
  desired_count         = var.services_desired_count
  
  environment_variables = {
    ENVIRONMENT = var.environment
  }
}

# Analytics Service
module "analytics_service" {
  source = "./modules/ecs-service"

  project_name          = var.project_name
  environment           = var.environment
  service_name          = "analytics"
  aws_region            = var.aws_region
  
  ecs_cluster_id        = aws_ecs_cluster.main.id
  ecs_cluster_name      = aws_ecs_cluster.main.name
  vpc_id                = module.vpc.vpc_id
  private_subnet_ids    = module.vpc.private_subnet_ids
  ecs_security_group_id = module.security_groups.ecs_security_group_id
  
  container_image       = "${var.ecr_repository_url}/analytics:${var.app_version}"
  container_port        = 8007
  container_cpu         = 512
  container_memory      = 1024
  desired_count         = var.services_desired_count
  
  environment_variables = {
    ENVIRONMENT = var.environment
  }
}

# Salesforce Service
module "salesforce_service" {
  source = "./modules/ecs-service"

  project_name          = var.project_name
  environment           = var.environment
  service_name          = "salesforce"
  aws_region            = var.aws_region
  
  ecs_cluster_id        = aws_ecs_cluster.main.id
  ecs_cluster_name      = aws_ecs_cluster.main.name
  vpc_id                = module.vpc.vpc_id
  private_subnet_ids    = module.vpc.private_subnet_ids
  ecs_security_group_id = module.security_groups.ecs_security_group_id
  
  container_image       = "${var.ecr_repository_url}/salesforce:${var.app_version}"
  container_port        = 8008
  container_cpu         = 256
  container_memory      = 512
  desired_count         = var.services_desired_count
  
  environment_variables = {
    ENVIRONMENT = var.environment
  }
}

# ==============================================================================
# S3 Module *********************************************************************
# ==============================================================================

module "s3_frontend" {
  source = "./modules/s3"

  project_name = var.project_name
  environment  = var.environment
  bucket_name  = "${var.project_name}-${var.environment}-frontend"
}

# ==============================================================================
# CloudFront Module *************************************************************
# ==============================================================================

module "cloudfront" {
  source = "./modules/cloudfront"

  project_name     = var.project_name
  environment      = var.environment
  s3_bucket_id     = module.s3_frontend.bucket_id
  s3_bucket_domain = module.s3_frontend.bucket_domain
  alb_domain_name  = module.alb.alb_dns_name
  
  enable_https     = var.enable_https
  certificate_arn  = var.cloudfront_certificate_arn
}

# ==============================================================================
# Secrets Manager ***************************************************************
# ==============================================================================

resource "aws_secretsmanager_secret" "db_password" {
  name        = "${var.project_name}-${var.environment}-db-password"
  description = "Database password for ${var.project_name}"

  tags = {
    Name = "${var.project_name}-db-password"
  }
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = var.db_password
}

# ==============================================================================
# CloudWatch Monitoring *********************************************************
# ==============================================================================

resource "aws_cloudwatch_log_group" "ecs_logs" {
  name              = "/ecs/${var.project_name}-${var.environment}"
  retention_in_days = var.log_retention_days

  tags = {
    Name = "${var.project_name}-ecs-logs"
  }
}

# ==============================================================================
# IAM Roles *********************************************************************
# ==============================================================================

# ECS Task Execution Role
resource "aws_iam_role" "ecs_task_execution" {
  name = "${var.project_name}-${var.environment}-ecs-task-execution"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution" {
  role       = aws_iam_role.ecs_task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# ECS Task Role
resource "aws_iam_role" "ecs_task" {
  name = "${var.project_name}-${var.environment}-ecs-task"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

# ==============================================================================
# Auto Scaling ******************************************************************
# ==============================================================================

resource "aws_appautoscaling_target" "ecs_target" {
  max_capacity       = var.max_capacity
  min_capacity       = var.min_capacity
  resource_id        = "service/${aws_ecs_cluster.main.name}/${module.gateway_service.service_name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "ecs_cpu" {
  name               = "${var.project_name}-cpu-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs_target.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value = 70.0
  }
}
