variable "REGION" {
  description = "AWS region to deploy resources into"
  type = string
  default = "eu-west-2"
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
  default     = "c19courtsdb"
}

variable "DB_USERNAME" {
  description = "Master username for RDS"
  type        = string
  default     = "courtsadmin"
}

variable "DB_PASSWORD" {
  description = "Master password for RDS"
  type        = string
  sensitive   = true
}

variable "SUBNET_IDS" {
  description = "List of subnet IDs for the DB subnet group"
  type        = list(string)
}