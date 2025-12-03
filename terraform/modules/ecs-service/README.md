# ECS Service Module

This module creates a complete ECS Fargate service with all necessary components for running containerized microservices in production.

## Features

- ✅ **ECS Fargate Service** - Serverless container orchestration
- ✅ **Task Definition** - Container configuration with environment variables and secrets
- ✅ **IAM Roles** - Separate execution and task roles with proper permissions
- ✅ **CloudWatch Logs** - Centralized logging with configurable retention
- ✅ **Auto Scaling** - CPU and memory-based scaling policies
- ✅ **Load Balancer Integration** - Optional ALB target group attachment
- ✅ **Service Discovery** - Optional AWS Cloud Map integration
- ✅ **Health Checks** - Container-level health monitoring
- ✅ **CloudWatch Alarms** - Optional high CPU/memory alerts
- ✅ **Deployment Circuit Breaker** - Automatic rollback on failures
- ✅ **ECS Exec Support** - Debug containers in production

## Usage

### Basic Example

```hcl
module "order_service" {
  source = "./modules/ecs-service"

  project_name          = "customer-portal"
  environment           = "production"
  service_name          = "order"
  
  ecs_cluster_id        = aws_ecs_cluster.main.id
  ecs_cluster_name      = aws_ecs_cluster.main.name
  vpc_id                = module.vpc.vpc_id
  private_subnet_ids    = module.vpc.private_subnet_ids
  ecs_security_group_id = module.security.ecs_sg_id
  
  container_image       = "123456789.dkr.ecr.us-west-2.amazonaws.com/order:latest"
  container_port        = 8001
  container_cpu         = 512
  container_memory      = 1024
  desired_count         = 2
  
  environment_variables = {
    DATABASE_URL = "postgresql://..."
    ENVIRONMENT  = "production"
  }
}
```

### With Load Balancer

```hcl
module "gateway_service" {
  source = "./modules/ecs-service"

  # ... basic config ...
  
  target_group_arn = aws_lb_target_group.gateway.arn
  
  enable_autoscaling = true
  min_capacity       = 1
  max_capacity       = 10
  cpu_target_value   = 70
}
```

### With Secrets Manager

```hcl
module "chatbot_service" {
  source = "./modules/ecs-service"

  # ... basic config ...
  
  environment_variables = {
    ENVIRONMENT = "production"
  }
  
  secrets = {
    OPENAI_API_KEY = aws_secretsmanager_secret.openai.arn
    DATABASE_PASS  = aws_secretsmanager_secret.db_pass.arn
  }
}
```

### With Custom Health Checks

```hcl
module "api_service" {
  source = "./modules/ecs-service"

  # ... basic config ...
  
  health_check = {
    command     = ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"]
    interval    = 30
    timeout     = 5
    retries     = 3
    start_period = 60
  }
}
```

### With CloudWatch Alarms

```hcl
module "critical_service" {
  source = "./modules/ecs-service"

  # ... basic config ...
  
  enable_alarms = true
  alarm_actions = [aws_sns_topic.alerts.arn]
}
```

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.0 |
| aws | ~> 5.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| project_name | Name of the project | string | - | yes |
| environment | Environment name | string | - | yes |
| service_name | Name of the microservice | string | - | yes |
| ecs_cluster_id | ID of the ECS cluster | string | - | yes |
| container_image | Docker image URI | string | - | yes |
| container_port | Container port | number | - | yes |
| vpc_id | VPC ID | string | - | yes |
| private_subnet_ids | Private subnet IDs | list(string) | - | yes |
| ecs_security_group_id | ECS security group ID | string | - | yes |
| container_cpu | CPU units (1024 = 1 vCPU) | number | 256 | no |
| container_memory | Memory in MB | number | 512 | no |
| desired_count | Desired task count | number | 1 | no |
| environment_variables | Environment variables | map(string) | {} | no |
| secrets | Secrets Manager/SSM secrets | map(string) | null | no |
| target_group_arn | ALB target group ARN | string | null | no |
| enable_autoscaling | Enable auto scaling | bool | true | no |
| min_capacity | Min task count | number | 1 | no |
| max_capacity | Max task count | number | 10 | no |
| cpu_target_value | CPU target % | number | 70 | no |
| enable_alarms | Enable CloudWatch alarms | bool | false | no |
| enable_ecs_exec | Enable ECS Exec | bool | false | no |
| log_retention_days | Log retention days | number | 7 | no |

## Outputs

| Name | Description |
|------|-------------|
| service_id | ECS service ID |
| service_name | ECS service name |
| service_arn | ECS service ARN |
| task_definition_arn | Task definition ARN |
| task_execution_role_arn | Execution role ARN |
| task_role_arn | Task role ARN |
| log_group_name | CloudWatch log group name |
| autoscaling_target_resource_id | Auto scaling target ID |

## Container CPU/Memory Options

Fargate supports specific CPU/memory combinations:

| CPU (vCPU) | Memory (GB) |
|------------|-------------|
| 0.25 (256) | 0.5, 1, 2 |
| 0.5 (512)  | 1, 2, 3, 4 |
| 1 (1024)   | 2, 3, 4, 5, 6, 7, 8 |
| 2 (2048)   | 4-16 (1GB increments) |
| 4 (4096)   | 8-30 (1GB increments) |

## Auto Scaling

The module supports CPU and memory-based auto scaling:

- **CPU Scaling**: Enabled by default, targets 70% utilization
- **Memory Scaling**: Optional, disabled by default
- **Scale Out**: 60 second cooldown
- **Scale In**: 300 second cooldown (5 minutes)

## Monitoring

### CloudWatch Logs
- Automatic log group creation
- Configurable retention (default: 7 days)
- Log stream prefix: `ecs`

### CloudWatch Alarms (Optional)
- High CPU (>80% for 10 minutes)
- High Memory (>80% for 10 minutes)
- SNS integration for alerts

## Debugging

Enable ECS Exec for shell access:

```hcl
enable_ecs_exec = true
```

Then use:
```bash
aws ecs execute-command \
  --cluster CLUSTER_NAME \
  --task TASK_ID \
  --container SERVICE_NAME \
  --interactive \
  --command "/bin/sh"
```

## Security

- **Execution Role**: Pulls images, writes logs, reads secrets
- **Task Role**: Application runtime permissions
- **Network**: Tasks run in private subnets with no public IP
- **Secrets**: Encrypted at rest in Secrets Manager

## Deployment Features

- **Circuit Breaker**: Automatically rolls back failed deployments
- **Rolling Updates**: 100% min healthy, 200% max capacity
- **Zero Downtime**: Drains connections before stopping tasks

## Cost Optimization

1. **Right-size containers**: Start small (256 CPU, 512 MB)
2. **Use Fargate Spot**: 70% cheaper (configure at cluster level)
3. **Reduce log retention**: Lower retention = lower costs
4. **Auto scaling**: Scale down during low traffic

## Examples

See the main Terraform configuration for complete examples of all 9 microservices.

## Notes

- Tasks automatically restart on failure
- Health checks run inside containers
- Logs are streamed to CloudWatch in real-time
- Auto scaling responds to CloudWatch metrics
- Deployment history is maintained in task definition revisions
