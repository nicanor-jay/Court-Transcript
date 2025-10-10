# 👾 Terraform scripts for easy AWS resource creation/deletion

These files contain all that is needed to set up our AWS resources on the cloud.

## 🛠️ Setup

We used a remote backend (S3 bucket) to collaborate more efficiently. This needs to be set up **manually** in the AWS UI. Once you do, you'll have to edit the bucket name in `terraform.tf` to match the one you've created.

If you won't be using a remote backend, make sure you **remove this code from `terraform.tf`**:

```
terraform {
  backend "s3" {
    bucket = "name-of-your-s3-bucket"
    key = "terraform.tfstate"
    region = "eu-west-2"
  }
}
```

Make sure to add a `terraform.tfvars` file in this folder with this format:
```
# Common to both modules
ACCESS_KEY = "your_aws_access_key"
SECRET_ACCESS_KEY = "your_aws_secret_key"
REGION ="your_aws_region"
DB_NAME = "your_db_name"
DB_USERNAME = "your_db_username"
DB_PASSWORD = "your_db_password"
SUBNET_IDS = "[list_of_subnet_ids]"
VPC_ID = "your_vpc_id"

# Phase one
DB_SUBNET_GROUP_NAME = "name_for_db_subnet_group_resource"
RDS_SECURITY_GROUP_NAME = "name_for_rds_security_group_resource"
COURTS_RDS_NAME = "name_for_rds_resource"
ECR_FOR_LAMBDA_NAME = "name_for_lambda_ecr"
ECR_FOR_DASHBOARD_NAME = "name_for_dashboard_ecr"

# Phase two
DB_PORT = "your_db_port"
DB_HOST = "your_rds_endpoint"
DASHBOARD_IMAGE_URI = "your_dashboard_image_uri"
ECS_CLUSTER = "your-ecs-cluster"
PIPELINE_IMAGE_URI = "your_pipeline_image_uri"


DASHBOARD_TASK_DEFINITION_NAME = "name_for_dashboard_task_definition_resource"
DASHBOARD_SECURITY_GROUP_NAME = "name_for_dashboard_security_group_resource"
DASHBOARD_ECS_SERVICE_NAME = "name_for_dashboard_ecs_service_resource"
LAMBDA_EXEC_ROLE_NAME = "name_for_lambda_exec_role_resource"
PIPELINE_LAMBDA_NAME = "name_for_pipeline_lambda_resource"
```

## 🚀 How to run

- If it's the first time, run `terraform init`.
- To create the resources needed for the first phase of the project, run `terraform apply -target=module.phase-one`.
- Then for the second phase, run `terraform apply -target=module.phase-two`.
- To destroy all resources, run `terraform destroy`.