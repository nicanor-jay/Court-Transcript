source .env

aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

docker buildx build . -t $PIPELINE_NAME:latest --platform "Linux/amd64" --provenance=false -f dockerfile

docker tag $PIPELINE_NAME:latest $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$PIPELINE_ECR_NAME:latest

docker push $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$PIPELINE_ECR_NAME:latest