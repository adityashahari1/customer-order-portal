# ============================================================================
# ECS Service Module - Outputs
# ============================================================================

output "service_id" {
  description = "ID of the ECS service"
  value       = aws_ecs_service.service.id
}

output "service_name" {
  description = "Name of the ECS service"
  value       = aws_ecs_service.service.name
}

output "service_arn" {
  description = "ARN of the ECS service"
  value       = aws_ecs_service.service.id
}

output "task_definition_arn" {
  description = "ARN of the task definition"
  value       = aws_ecs_task_definition.service.arn
}

output "task_definition_family" {
  description = "Family of the task definition"
  value       = aws_ecs_task_definition.service.family
}

output "task_definition_revision" {
  description = "Revision of the task definition"
  value       = aws_ecs_task_definition.service.revision
}

output "task_execution_role_arn" {
  description = "ARN of the task execution IAM role"
  value       = aws_iam_role.task_execution.arn
}

output "task_execution_role_name" {
  description = "Name of the task execution IAM role"
  value       = aws_iam_role.task_execution.name
}

output "task_role_arn" {
  description = "ARN of the task IAM role"
  value       = aws_iam_role.task.arn
}

output "task_role_name" {
  description = "Name of the task IAM role"
  value       = aws_iam_role.task.name
}

output "log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.service.name
}

output "log_group_arn" {
  description = "ARN of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.service.arn
}

output "autoscaling_target_resource_id" {
  description = "Resource ID of the autoscaling target"
  value       = var.enable_autoscaling ? aws_appautoscaling_target.service[0].resource_id : null
}

output "cpu_autoscaling_policy_arn" {
  description = "ARN of the CPU autoscaling policy"
  value       = var.enable_autoscaling ? aws_appautoscaling_policy.cpu[0].arn : null
}

output "memory_autoscaling_policy_arn" {
  description = "ARN of the memory autoscaling policy"
  value       = var.enable_autoscaling && var.enable_memory_scaling ? aws_appautoscaling_policy.memory[0].arn : null
}

output "high_cpu_alarm_arn" {
  description = "ARN of the high CPU CloudWatch alarm"
  value       = var.enable_alarms ? aws_cloudwatch_metric_alarm.high_cpu[0].arn : null
}

output "high_memory_alarm_arn" {
  description = "ARN of the high memory CloudWatch alarm"
  value       = var.enable_alarms ? aws_cloudwatch_metric_alarm.high_memory[0].arn : null
}
