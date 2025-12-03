# ============================================================================
# ECS Service Module
# ============================================================================
# Creates an ECS Fargate service with task definition, auto-scaling,
# CloudWatch logging, and ALB integration
# ============================================================================

# ============================================================================
# CloudWatch Log Group
# ============================================================================

resource "aws_cloudwatch_log_group" "service" {
  name              = "/ecs/${var.project_name}-${var.environment}/${var.service_name}"
  retention_in_days = var.log_retention_days

  tags = {
    Name        = "${var.project_name}-${var.service_name}-logs"
    Service     = var.service_name
    Environment = var.environment
  }
}

# ============================================================================
# IAM Roles
# ============================================================================

# ECS Task Execution Role (for pulling images, writing logs)
resource "aws_iam_role" "task_execution" {
  name = "${var.project_name}-${var.environment}-${var.service_name}-exec"

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

  tags = {
    Name    = "${var.project_name}-${var.service_name}-execution-role"
    Service = var.service_name
  }
}

resource "aws_iam_role_policy_attachment" "task_execution" {
  role       = aws_iam_role.task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Additional policy for Secrets Manager and ECR
resource "aws_iam_role_policy" "task_execution_extras" {
  name = "${var.project_name}-${var.environment}-${var.service_name}-exec-extras"
  role = aws_iam_role.task_execution.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "kms:Decrypt"
        ]
        Resource = "*"
      }
    ]
  })
}

# ECS Task Role (for application runtime permissions)
resource "aws_iam_role" "task" {
  name = "${var.project_name}-${var.environment}-${var.service_name}-task"

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

  tags = {
    Name    = "${var.project_name}-${var.service_name}-task-role"
    Service = var.service_name
  }
}

# Task role policy for service-specific permissions
resource "aws_iam_role_policy" "task_policy" {
  count = var.task_role_policy != null ? 1 : 0
  name  = "${var.project_name}-${var.environment}-${var.service_name}-task-policy"
  role  = aws_iam_role.task.id

  policy = var.task_role_policy
}

# ============================================================================
# ECS Task Definition
# ============================================================================

resource "aws_ecs_task_definition" "service" {
  family                   = "${var.project_name}-${var.environment}-${var.service_name}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.container_cpu
  memory                   = var.container_memory
  execution_role_arn       = aws_iam_role.task_execution.arn
  task_role_arn            = aws_iam_role.task.arn

  container_definitions = jsonencode([
    {
      name      = var.service_name
      image     = var.container_image
      essential = true

      portMappings = [
        {
          containerPort = var.container_port
          hostPort      = var.container_port
          protocol      = "tcp"
        }
      ]

      environment = [
        for key, value in var.environment_variables : {
          name  = key
          value = tostring(value)
        }
      ]

      secrets = var.secrets != null ? [
        for key, value in var.secrets : {
          name      = key
          valueFrom = value
        }
      ] : []

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.service.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }

      healthCheck = var.health_check != null ? {
        command     = var.health_check.command
        interval    = var.health_check.interval
        timeout     = var.health_check.timeout
        retries     = var.health_check.retries
        startPeriod = var.health_check.start_period
      } : null
    }
  ])

  tags = {
    Name        = "${var.project_name}-${var.service_name}-task"
    Service     = var.service_name
    Environment = var.environment
  }
}

# ============================================================================
# ECS Service
# ============================================================================

resource "aws_ecs_service" "service" {
  name            = "${var.project_name}-${var.environment}-${var.service_name}"
  cluster         = var.ecs_cluster_id
  task_definition = aws_ecs_task_definition.service.arn
  desired_count   = var.desired_count
  launch_type     = var.launch_type

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [var.ecs_security_group_id]
    assign_public_ip = false
  }

  # Load balancer configuration (optional)
  dynamic "load_balancer" {
    for_each = var.target_group_arn != null ? [1] : []
    content {
      target_group_arn = var.target_group_arn
      container_name   = var.service_name
      container_port   = var.container_port
    }
  }

  # Service discovery configuration (optional)
  dynamic "service_registries" {
    for_each = var.service_discovery_arn != null ? [1] : []
    content {
      registry_arn = var.service_discovery_arn
    }
  }

  # Deployment configuration
  deployment_configuration {
    maximum_percent         = 200
    minimum_healthy_percent = 100
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  # Enable ECS Exec for debugging
  enable_execute_command = var.enable_ecs_exec

  # Fargate platform version
  platform_version = "LATEST"

  # Propagate tags from task definition
  propagate_tags = "TASK_DEFINITION"

  # Wait for steady state (optional, useful for CI/CD)
  wait_for_steady_state = var.wait_for_steady_state

  tags = {
    Name        = "${var.project_name}-${var.service_name}-service"
    Service     = var.service_name
    Environment = var.environment
  }

  # Lifecycle to prevent unnecessary recreation
  lifecycle {
    ignore_changes = [desired_count]
  }

  # Depends on IAM roles being created
  depends_on = [
    aws_iam_role_policy_attachment.task_execution,
    aws_iam_role_policy.task_execution_extras
  ]
}

# ============================================================================
# Auto Scaling
# ============================================================================

resource "aws_appautoscaling_target" "service" {
  count              = var.enable_autoscaling ? 1 : 0
  max_capacity       = var.max_capacity
  min_capacity       = var.min_capacity
  resource_id        = "service/${var.ecs_cluster_name}/${aws_ecs_service.service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

# CPU-based auto-scaling
resource "aws_appautoscaling_policy" "cpu" {
  count              = var.enable_autoscaling ? 1 : 0
  name               = "${var.project_name}-${var.service_name}-cpu-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.service[0].resource_id
  scalable_dimension = aws_appautoscaling_target.service[0].scalable_dimension
  service_namespace  = aws_appautoscaling_target.service[0].service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value       = var.cpu_target_value
    scale_in_cooldown  = var.scale_in_cooldown
    scale_out_cooldown = var.scale_out_cooldown
  }
}

# Memory-based auto-scaling
resource "aws_appautoscaling_policy" "memory" {
  count              = var.enable_autoscaling && var.enable_memory_scaling ? 1 : 0
  name               = "${var.project_name}-${var.service_name}-memory-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.service[0].resource_id
  scalable_dimension = aws_appautoscaling_target.service[0].scalable_dimension
  service_namespace  = aws_appautoscaling_target.service[0].service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageMemoryUtilization"
    }
    target_value       = var.memory_target_value
    scale_in_cooldown  = var.scale_in_cooldown
    scale_out_cooldown = var.scale_out_cooldown
  }
}

# ============================================================================
# CloudWatch Alarms (Optional)
# ============================================================================

resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  count               = var.enable_alarms ? 1 : 0
  alarm_name          = "${var.project_name}-${var.service_name}-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors ECS CPU utilization"
  alarm_actions       = var.alarm_actions

  dimensions = {
    ClusterName = var.ecs_cluster_name
    ServiceName = aws_ecs_service.service.name
  }

  tags = {
    Name    = "${var.project_name}-${var.service_name}-high-cpu-alarm"
    Service = var.service_name
  }
}

resource "aws_cloudwatch_metric_alarm" "high_memory" {
  count               = var.enable_alarms ? 1 : 0
  alarm_name          = "${var.project_name}-${var.service_name}-high-memory"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "MemoryUtilization"
  namespace           = "AWS/ECS"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors ECS memory utilization"
  alarm_actions       = var.alarm_actions

  dimensions = {
    ClusterName = var.ecs_cluster_name
    ServiceName = aws_ecs_service.service.name
  }

  tags = {
    Name    = "${var.project_name}-${var.service_name}-high-memory-alarm"
    Service = var.service_name
  }
}
