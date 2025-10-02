terraform {
  backend "s3" {
    bucket = "c19-courts-terraform-state"
    key = "terraform.tfstate"
    region = "eu-west-2"
  }
}

provider "aws" {
    region = var.REGION
    access_key = var.ACCESS_KEY
    secret_key = var.SECRET_ACCESS_KEY
}