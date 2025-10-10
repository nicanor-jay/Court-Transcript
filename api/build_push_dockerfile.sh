source .env

aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

docker buildx build . -t "$ECR_FOR_API_NAME":latest --platform "Linux/amd64" --provenance=false

docker tag "$ECR_FOR_API_NAME":latest $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/"$ECR_FOR_API_NAME":latest

docker push $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/"$ECR_FOR_API_NAME":latest