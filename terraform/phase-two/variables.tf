# Common to both modules

variable "REGION" {
  description = "AWS region to deploy resources into"
  type = string
}

variable "ACCESS_KEY" {
  description = "AWS access key"
  type = string
}

variable "SECRET_ACCESS_KEY" {
  description = "AWS secret access key"
  type = string
}

variable "DB_NAME" {
  description = "Database name (must not contain dashes)"
  type        = string
}

variable "DB_USERNAME" {
  description = "Master username for RDS"
  type        = string
}

variable "DB_PASSWORD" {
  description = "Master password for RDS"
  type        = string
  sensitive   = true
}

variable "VPC_ID" {
  description = "VPC ID for the RDS instance"
  type = string
}

variable "SUBNET_IDS" {
  description = "List of subnet IDs for the DB subnet group"
  type        = list(string)
}


# Specific to this module

variable "DB_PORT" {
  description = "Port for our DB"
  type        = string
}

variable "DB_HOST" {
  description = "Endpoint of our RDS instance"
  type        = string
}

variable "DASHBOARD_IMAGE_URI" {
  description = "URI for the dashboard image"
  type        = string
}

variable "PIPELINE_IMAGE_URI" {
  description = "URI for the pipeline image"
  type        = string
}

variable "EMAIL_IMAGE_URI" {
  description = "URI for the email image"
  type        = string
}

variable "ECS_CLUSTER" {
  description = "ARN of ECS cluster to use for the dashboard ECS service"
  type        = string
}

variable "OPENAI_API_KEY" {
  description = "GPT-API key"
  type        = string
}

variable "DASHBOARD_TASK_DEFINITION_NAME" {
  description = "Name for the dashboard's task definition resource"
  type        = string
}

variable "DASHBOARD_SECURITY_GROUP_NAME" {
  description = "Name for the dashboard's security group resource"
  type        = string
}

variable "DASHBOARD_ECS_SERVICE_NAME" {
  description = "Name for the dashboard's ECS service resource"
  type        = string
}

variable "LAMBDA_EXEC_ROLE_NAME" {
  description = "Name for the lambda's execution role"
  type        = string
}

variable "PIPELINE_LAMBDA_NAME" {
  description = "Name for the pipeline lambda"
  type        = string
}

variable "EMAIL_LAMBDA_NAME" {
  description = "Name for the email services lambda"
  type        = string
}