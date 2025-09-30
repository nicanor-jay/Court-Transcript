module "phase-one" {
    source = "./phase-one"
    ACCESS_KEY = var.ACCESS_KEY
    SECRET_ACCESS_KEY = var.SECRET_ACCESS_KEY
    REGION = var.REGION
}

module "phase-two" {
    source = "./phase-two"
    ACCESS_KEY = var.ACCESS_KEY
    SECRET_ACCESS_KEY = var.SECRET_ACCESS_KEY
    REGION = var.REGION
}