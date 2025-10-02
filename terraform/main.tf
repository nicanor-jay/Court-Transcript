module "phase-one" {
    source = "./phase-one"
    ACCESS_KEY = var.ACCESS_KEY
    SECRET_ACCESS_KEY = var.SECRET_ACCESS_KEY
    REGION = var.REGION
    DB_NAME = var.DB_NAME
    DB_USERNAME = var.DB_USERNAME
    DB_PASSWORD = var.DB_PASSWORD
    VPC_ID = var.VPC_ID
    SUBNET_IDS = var.SUBNET_IDS
}

module "phase-two" {
    source = "./phase-two"
    ACCESS_KEY = var.ACCESS_KEY
    SECRET_ACCESS_KEY = var.SECRET_ACCESS_KEY
    REGION = var.REGION
    DB_NAME = var.DB_NAME
    DB_USERNAME = var.DB_USERNAME
    DB_PASSWORD = var.DB_PASSWORD
    VPC_ID = var.VPC_ID
    SUBNET_IDS = var.SUBNET_IDS
    RDS_ENDPOINT = var.RDS_ENDPOINT
    DASHBOARD_IMAGE_URI = var.DASHBOARD_IMAGE_URI
    ECS_CLUSTER = var.ECS_CLUSTER
}