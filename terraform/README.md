# 👾 Terraform Scripts for AWS Resource Management

Automated infrastructure setup for the C19 Courts project using Terraform.

---

## 📖 Overview

These Terraform scripts automate the creation and management of all required AWS resources for the C19 Courts application, including RDS databases, ECS services, Lambda functions, and EventBridge schedulers.

---

## 🛠️ Prerequisites

- Terraform installed (v1.0+)
- AWS CLI configured with appropriate credentials
- An AWS account with necessary permissions

---

## ⚙️ Initial Setup

### 1. Remote Backend Configuration (Optional but Recommended)

For team collaboration, we use an S3 bucket as a remote backend. This must be created **manually** in the AWS Console.

After creating your S3 bucket, update the bucket name in `terraform.tf`:

```hcl
terraform {
  backend "s3" {
    bucket = "your-terraform-state-bucket"
    key    = "terraform.tfstate"
    region = "eu-west-2"
  }
}
```

**Note:** If you're working solo or don't need a remote backend, remove the entire `backend "s3"` block from `terraform.tf`.

### 2. Configure Variables

Create a `terraform.tfvars` file in the root directory with your AWS configuration:

```hcl
# ==========================================
# AWS Credentials & Core Configuration
# ==========================================
ACCESS_KEY        = "your_aws_access_key"
SECRET_ACCESS_KEY = "your_aws_secret_key"
REGION            = "eu-west-2"
VPC_ID            = "vpc-xxxxxxxxxxxxxxxxx"
SUBNET_IDS        = ["subnet-xxxxxxxxxxxxxxxxx", "subnet-xxxxxxxxxxxxxxxxx", "subnet-xxxxxxxxxxxxxxxxx"]

# ==========================================
# Database Configuration
# ==========================================
DB_NAME     = "your_database_name"
DB_USERNAME = "your_db_username"
DB_PASSWORD = "your_secure_password"
DB_PORT     = "5432"
DB_HOST     = "your-rds-endpoint.xxxxxxxxx.eu-west-2.rds.amazonaws.com"

# ==========================================
# Phase One: Base Infrastructure
# ==========================================
DB_SUBNET_GROUP_NAME    = "your-db-subnet-group-name"
RDS_SECURITY_GROUP_NAME = "your-rds-security-group-name"
COURTS_RDS_NAME         = "your-rds-instance-name"
ECR_FOR_LAMBDA_NAME     = "your-lambda-ecr-name"
ECR_FOR_DASHBOARD_NAME  = "your-dashboard-ecr-name"
ECR_FOR_API_NAME        = "your-api-ecr-name"
ECR_FOR_EMAIL_NAME      = "your-email-ecr-name"

# ==========================================
# Phase Two: Application Services
# ==========================================
ECS_CLUSTER = "your-ecs-cluster-name"

# Docker Image URIs
DASHBOARD_IMAGE_URI = "xxxxxxxxxxxx.dkr.ecr.eu-west-2.amazonaws.com/your-dashboard-repo:latest"
API_IMAGE_URI       = "xxxxxxxxxxxx.dkr.ecr.eu-west-2.amazonaws.com/your-api-repo:latest"
PIPELINE_IMAGE_URI  = "xxxxxxxxxxxx.dkr.ecr.eu-west-2.amazonaws.com/your-pipeline-repo:latest"
EMAIL_IMAGE_URI     = "xxxxxxxxxxxx.dkr.ecr.eu-west-2.amazonaws.com/your-email-repo:latest"

# Dashboard Service
DASHBOARD_TASK_DEFINITION_NAME = "your-dashboard-task-definition-name"
DASHBOARD_SECURITY_GROUP_NAME  = "your-dashboard-security-group-name"
DASHBOARD_ECS_SERVICE_NAME     = "your-dashboard-service-name"

# API Service
API_TASK_DEFINITION_NAME = "your-api-task-definition-name"
API_SECURITY_GROUP_NAME  = "your-api-security-group-name"
API_ECS_SERVICE_NAME     = "your-api-service-name"

# Lambda Functions
LAMBDA_EXEC_ROLE_NAME = "your-lambda-execution-role-name"
PIPELINE_LAMBDA_NAME  = "your-pipeline-lambda-name"
EMAIL_LAMBDA_NAME     = "your-email-lambda-name"

# EventBridge Schedulers
PIPELINE_SCHEDULER_ROLE_NAME   = "your-pipeline-scheduler-role-name"
PIPELINE_SCHEDULER_POLICY_NAME = "your-pipeline-scheduler-policy-name"
PIPELINE_SCHEDULER_NAME        = "your-pipeline-scheduler-name"

EMAIL_SCHEDULER_ROLE_NAME   = "your-email-scheduler-role-name"
EMAIL_SCHEDULER_POLICY_NAME = "your-email-scheduler-policy-name"
EMAIL_SCHEDULER_NAME        = "your-email-scheduler-name"

# External Services
OPENAI_API_KEY = ""
ORIGIN_EMAIL   = "your-verified-email@example.com"
```

---

## 🚀 Deployment Instructions

### Step 1: Initialize Terraform

Run this command the first time you use Terraform in this directory:

```bash
terraform init
```

### Step 2: Deploy Phase One (Base Infrastructure)

Create the foundational resources (RDS, ECR repositories):

```bash
terraform apply -target=module.phase-one
```

Review the planned changes and type `yes` to confirm.

### Step 3: Deploy Phase Two (Application Services)

After Phase One completes, deploy the application layer (ECS services, Lambdas, schedulers):

```bash
terraform apply -target=module.phase-two
```

Review the planned changes and type `yes` to confirm.

### Step 4: Verify Deployment

Check the AWS Console to ensure all resources are running correctly:
- RDS database is available
- ECS services are running
- Lambda functions are deployed
- EventBridge schedulers are active

---

## 🗑️ Teardown

To destroy all created resources:

```bash
terraform destroy
```

**Warning:** This will permanently delete all resources. Ensure you have backups if needed.

---

## 📦 Resources Created

### Phase One: Base Infrastructure

| Resource Type | Purpose |
|--------------|---------|
| **RDS PostgreSQL** | Primary database instance |
| **DB Subnet Group** | Network configuration for RDS |
| **RDS Security Group** | Firewall rules for database access |
| **ECR Repositories** | Docker image storage for Lambda, Dashboard, API, and Email services |

### Phase Two: Application Services

| Resource Type | Purpose |
|--------------|---------|
| **ECS Task Definitions** | Container configurations for Dashboard and API |
| **ECS Services** | Managed container deployments |
| **Security Groups** | Network access control for ECS services |
| **Lambda Functions** | Serverless functions for pipeline and email tasks |
| **IAM Roles & Policies** | Permissions for Lambda and EventBridge |
| **EventBridge Schedulers** | Automated triggers for pipeline and email tasks |

---

## 🔒 Security Notes

- **Never commit `terraform.tfvars`** to version control (it's in `.gitignore`)
- Store sensitive credentials in AWS Secrets Manager or use environment variables
- Ensure your AWS user has appropriate IAM permissions
- Review security group rules before deployment
- The ORIGIN_EMAIL must be verified in AWS SES before use

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** `Error: No valid credential sources found`
- **Solution:** Ensure AWS CLI is configured or `ACCESS_KEY` and `SECRET_ACCESS_KEY` are set correctly

**Issue:** `Error: subnet not found`
- **Solution:** Verify the `SUBNET_IDS` exist in your specified VPC

**Issue:** `Error: Backend initialization required`
- **Solution:** Run `terraform init` before applying changes

**Issue:** Lambda function fails to deploy
- **Solution:** Ensure Docker images are pushed to ECR before running Phase Two

---