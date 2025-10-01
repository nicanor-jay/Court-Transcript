# DB subnet group
resource "aws_db_subnet_group" "c19_courts_db_subnet_group" {
  name       = "c19-courts-db-subnet-group"
  subnet_ids = var.SUBNET_IDS

  tags = {
    Name = "c19-courts-db-subnet-group"
  }
}

# DB instance
resource "aws_db_instance" "c19_courts_db" {
  identifier        = "c19-courts-db"
  engine            = "postgres"
  instance_class    = "db.t3.micro"
  allocated_storage = 20

  db_name   = var.DB_NAME
  username  = var.DB_USERNAME
  password  = var.DB_PASSWORD

  db_subnet_group_name = aws_db_subnet_group.c19_courts_db_subnet_group.name
  publicly_accessible  = true
  skip_final_snapshot  = true
}

# ECR to host lambda
resource "aws_ecr_repository" "lambda-ecr" {
  name                 = "c19-courts-daily-pipeline"
  image_tag_mutability = "MUTABLE"
}

# ECR to host the ECS Task
resource "aws_ecr_repository" "ecs-ecr" {
  name                 = "c19-courts-ecs-task"
  image_tag_mutability = "MUTABLE"
}

# ECR to host the ECS Dashboard
resource "aws_ecr_repository" "dashboard-ecr" {
  name                 = "c19-courts-dashboard-service"
  image_tag_mutability = "MUTABLE"
}