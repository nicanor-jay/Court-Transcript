source .env

aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

docker buildx build . -t $EMAIL_ECR_NAME:latest --platform "Linux/amd64" --provenance=false -f Dockerfile

docker tag $EMAIL_ECR_NAME:latest $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$EMAIL_ECR_NAME:latest

docker push $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$EMAIL_ECR_NAME:latest