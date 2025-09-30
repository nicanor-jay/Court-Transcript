resource "aws_ecr_repository" "project-ecr" {
  name                 = "c19-courts-daily-pipeline"
  image_tag_mutability = "MUTABLE"
}