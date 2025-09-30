provider "aws" {
  region = var.aws_region
}

resource "aws_db_subnet_group" "c19_courts_db_subnet_group" {
  name       = "c19-courts-db-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    Name = "c19-courts-db-subnet-group"
  }
}

resource "aws_db_instance" "c19_courts_db" {
  identifier        = "c19-courts-db"
  engine            = "postgres"
  instance_class    = "db.t3.micro"
  allocated_storage = 20

  db_name   = var.db_name
  username  = var.db_username
  password  = var.db_password

  db_subnet_group_name = aws_db_subnet_group.c19_courts_db_subnet_group.name
  publicly_accessible  = true
  skip_final_snapshot  = true
}
