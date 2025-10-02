# ECS task definition (dashboard)
resource "aws_ecs_task_definition" "c19-courts-dashboard-td" {
  family = "c19-courts-dashboard-td"
  requires_compatibilities = ["FARGATE"]
  network_mode = "awsvpc"
  cpu = 1024
  memory = 2048
  execution_role_arn = "arn:aws:iam::129033205317:role/ecsTaskExecutionRole"
  container_definitions = jsonencode([
    {
        name = "pipeline"
        image = var.DASHBOARD_IMAGE_URI
        memory = 128
        environment = [
            {name = "ACCESS_KEY", value = var.ACCESS_KEY},
            {name = "SECRET_ACCESS_KEY", value = var.SECRET_ACCESS_KEY},
            {name = "RDS_ENDPOINT", value = var.RDS_ENDPOINT},
            {name = "DB_USERNAME", value = var.DB_USERNAME},
            {name = "DB_PASSWORD", value = var.DB_PASSWORD},
            {name = "DB_NAME", value = var.DB_NAME}
        ],
        logConfiguration = {
            logDriver = "awslogs"
            options = {
                "awslogs-group" = "/ecs/"
                "awslogs-region" = var.REGION
                "awslogs-stream-prefix" = "ecs"
                "awslogs-create-group" = "true"
            }
        }
    }

  ])
}

# Security group (dashboard)
resource "aws_security_group" "courts_dashboard_security_group" {
    name = "c19-courts-dashboard-sg"
    description = "Allow inbound traffic to an RDS instance"
    vpc_id = var.VPC_ID

    ingress {
        description = "Allow traffic on port 8501"
        from_port = 8501
        to_port = 8501
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
        from_port        = 0
        to_port          = 0
        protocol         = "-1"
        cidr_blocks      = ["0.0.0.0/0"]
    }
}

# ECS service (dashboard)
resource "aws_ecs_service" "c19-courts-dashboard-service" {
  name = "c19-courts-dashboard-service"
  cluster = var.ECS_CLUSTER
  task_definition = aws_ecs_task_definition.c19-courts-dashboard-td.arn
  desired_count = 1
  launch_type = "FARGATE"
  network_configuration {
    subnets = var.SUBNET_IDS
    security_groups = [aws_security_group.courts_dashboard_security_group.id]
    assign_public_ip = true
  }
}