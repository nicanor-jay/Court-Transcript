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
        ]
    }

  ])
}