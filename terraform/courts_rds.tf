provider "aws" {
  region = "eu-west-2"
}

# Subnet group for RDS
resource "aws_db_subnet_group" "c19_courts_db_subnet_group" {
  name       = "c19-courts-db-subnet-group"
  subnet_ids = [
    "subnet-00506a8db091bdf2a",
    "subnet-0425a4a0b929ea507",
    "subnet-0e7a1e60734c4fca7"
  ]
}

# PostgreSQL RDS Instance
resource "aws_db_instance" "c19_courts_db" {
  identifier        = "c19-courts-db"
  engine            = "postgres"
  instance_class    = "db.t3.micro"
  allocated_storage = 20

  db_name   = "c19courtsdb"
  username  = "courtsadmin"
  password  = "courtspassword"

  db_subnet_group_name = aws_db_subnet_group.c19_courts_db_subnet_group.name

  publicly_accessible = true
  skip_final_snapshot = true
}

# Output the endpoint
output "c19_courts_db_endpoint" {
  value     = aws_db_instance.c19_courts_db.endpoint
  sensitive = true
}
