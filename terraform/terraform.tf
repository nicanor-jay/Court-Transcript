terraform {
  backend "s3" {
    bucket = "c19-courts-terraform-state"
    key = "terraform.tfstate"
    region = "eu-west-2"
  }
}
