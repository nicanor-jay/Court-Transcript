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

variable "DB_SUBNET_GROUP_NAME" {
  description = "Name for the RDS subnet resource"
  type = string
}

variable "RDS_SECURITY_GROUP_NAME" {
  description = "Name for the RDS security group resource"
  type = string
}

variable "COURTS_RDS_NAME" {
  description = "Name for the courts RDS resource"
  type = string
}

variable "ECR_FOR_LAMBDA_NAME" {
  description = "Name for the ECR hosting our lambda image"
  type = string
}

variable "ECR_FOR_EMAIL_NAME" {
  description = "Name for the ECR hosting our email image"
  type = string
}

variable "ECR_FOR_DASHBOARD_NAME" {
  description = "Name for the ECR hosting our dashboard image"
  type = string
}