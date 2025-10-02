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

variable "DB_PORT" {
  description = "Port for our DB"
  type        = string
}

variable "DB_HOST" {
  description = "Endpoint of our RDS instance"
  type        = string
}

variable "VPC_ID" {
  description = "VPC ID for the RDS instance"
  type = string
}

variable "SUBNET_IDS" {
  description = "List of subnet IDs for the DB subnet group"
  type        = list(string)
}

variable "DASHBOARD_IMAGE_URI" {
  description = "URI for the dashboard image"
  type        = string
}

variable "ECS_CLUSTER" {
  description = "ARN of ECS cluster to use for the dashboard ECS service"
  type        = string
}