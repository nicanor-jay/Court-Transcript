# ECS task definition (dashboard)
resource "aws_ecs_task_definition" "courts-dashboard-td" {
  family = var.DASHBOARD_TASK_DEFINITION_NAME
  requires_compatibilities = ["FARGATE"]
  network_mode = "awsvpc"
  cpu = 1024
  memory = 2048
  execution_role_arn = "arn:aws:iam::129033205317:role/ecsTaskExecutionRole"
  container_definitions = jsonencode([
    {
        name = "dashboard"
        image = var.DASHBOARD_IMAGE_URI
        memory = 128
        environment = [
            {name = "ACCESS_KEY", value = var.ACCESS_KEY},
            {name = "SECRET_ACCESS_KEY", value = var.SECRET_ACCESS_KEY},
            {name = "DB_PORT", value = var.DB_PORT},
            {name = "DB_HOST", value = var.DB_HOST},
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
    name = var.DASHBOARD_SECURITY_GROUP_NAME
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
resource "aws_ecs_service" "courts-dashboard-service" {
  name = var.DASHBOARD_ECS_SERVICE_NAME
  cluster = var.ECS_CLUSTER
  task_definition = aws_ecs_task_definition.courts-dashboard-td.arn
  desired_count = 1
  launch_type = "FARGATE"
  network_configuration {
    subnets = var.SUBNET_IDS
    security_groups = [aws_security_group.courts_dashboard_security_group.id]
    assign_public_ip = true
  }
}

## LAMBDA, ROLE AND CLOUDWATCH

# Role for lambda
resource "aws_iam_role" "lambda_exec_role" {
 name = var.LAMBDA_EXEC_ROLE_NAME
  assume_role_policy = jsonencode({
   Version = "2012-10-17",
   Statement = [
     {
       Action = "sts:AssumeRole",
       Principal = {
         Service = [
          "lambda.amazonaws.com"
         ]
       },
       Effect = "Allow"
     }
   ]
  })
}
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
 role       = aws_iam_role.lambda_exec_role.name
 policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Cloudwatch log group
resource "aws_cloudwatch_log_group" "lambda_cloudwatch" {
  name              = "/aws/lambda/${var.PIPELINE_LAMBDA_NAME}"
  retention_in_days = 14

  tags = {
    Environment = "production"
    Application = "pipeline-lambda"
  }
}

# Pipeline Lambda
resource "aws_lambda_function" "courts-lambda" {
  function_name = var.PIPELINE_LAMBDA_NAME
  role          = aws_iam_role.lambda_exec_role.arn
  package_type  = "Image"
  image_uri     = var.PIPELINE_IMAGE_URI
  memory_size = 512
  timeout     = 300
  logging_config {
    log_format            = "JSON"
    application_log_level = "INFO"
    system_log_level      = "WARN"
  }

  depends_on = [aws_cloudwatch_log_group.lambda_cloudwatch]

  environment {
    variables = {
      DB_HOST=var.DB_HOST
      DB_PORT=var.DB_PORT
      DB_USERNAME=var.DB_USERNAME
      DB_PASSWORD=var.DB_PASSWORD
      DB_NAME=var.DB_NAME
    }
  }
  architectures = ["x86_64"]
}