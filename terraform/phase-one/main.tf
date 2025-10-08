# DB subnet group
resource "aws_db_subnet_group" "courts_db_subnet_group" {
  name       = var.DB_SUBNET_GROUP_NAME
  subnet_ids = var.SUBNET_IDS

  tags = {
    Name = var.DB_SUBNET_GROUP_NAME
  }
}

# Security group
resource "aws_security_group" "courts_rds_security_group" {
    name = var.RDS_SECURITY_GROUP_NAME
    description = "Allow inbound traffic to an RDS instance"
    vpc_id = var.VPC_ID

    ingress {
        description = "Postgres access from the internet"
        from_port = 5432
        to_port = 5432
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

# DB instance
resource "aws_db_instance" "courts_db" {
  identifier        = var.COURTS_RDS_NAME
  engine            = "postgres"
  instance_class    = "db.t3.micro"
  allocated_storage = 20

  db_name   = var.DB_NAME
  username  = var.DB_USERNAME
  password  = var.DB_PASSWORD

  vpc_security_group_ids = [aws_security_group.courts_rds_security_group.id]
  db_subnet_group_name = aws_db_subnet_group.courts_db_subnet_group.name
  publicly_accessible  = true
  skip_final_snapshot  = true
}

# ECR to host lambda
resource "aws_ecr_repository" "lambda-ecr" {
  name                 = var.ECR_FOR_LAMBDA_NAME
  image_tag_mutability = "MUTABLE"
}

# ECR to host the email image
resource "aws_ecr_repository" "email-ecr" {
  name                 = var.ECR_FOR_EMAIl_NAME
  image_tag_mutability = "MUTABLE"
}

# ECR to host the ECS Dashboard
resource "aws_ecr_repository" "dashboard-ecr" {
  name                 = var.ECR_FOR_DASHBOARD_NAME
  image_tag_mutability = "MUTABLE"
}