variable "aws_region" {
  description = "AWS region to deploy resources into"
  type        = string
  default     = "eu-west-2"
}

variable "db_name" {
  description = "Database name (must not contain dashes)"
  type        = string
  default     = "c19courtsdb"
}

variable "db_username" {
  description = "Master username for RDS"
  type        = string
  default     = "courtsadmin"
}

variable "db_password" {
  description = "Master password for RDS"
  type        = string
  sensitive   = true
  default     = "courtspassword"
}
