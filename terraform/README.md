# 👾 Terraform scripts for easy AWS resource creation/deletion

These files contain all that is needed to set up our AWS resources on the cloud.

## 🛠️ Setup

We used a remote backend (S3 bucket) to collaborate more efficiently. This needs to be set up **manually** in the AWS UI.

If you won't be using a remote backend, make sure you **remove this code from `terraform.tf`**:

```
terraform {
  backend "s3" {
    bucket = "c19-courts-terraform-state"
    key = "terraform.tfstate"
    region = "eu-west-2"
  }
}
```

Make sure to add a `terraform.tfvars` file in this folder with your AWS access key, AWS secret access key, DB password and DB subnet IDs in this format:
```
ACCESS_KEY = "your_aws_access_key"
SECRET_ACCESS_KEY = "your_aws_secret_key"
DB_PASSWORD = "your_db_password"
SUBNET_IDS = "[list_of_subnet_ids]"

```

## 🚀 How to run

- If it's the first time, run `terraform init`.
- To create the resources needed for the first phase of the project, run `terraform apply -target=module.phase-one`.
- Then for the second phase, run `terraform apply -target=module.phase-two`.
- To destroy all resources, run `terraform destroy`.