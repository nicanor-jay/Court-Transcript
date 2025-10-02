source ../.env

aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

docker buildx build . -t $APP_NAME:latest --platform "Linux/amd64"

docker tag $APP_NAME:latest $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$DASHBOARD_ECR_NAME:latest

docker push $AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$DASHBOARD_ECR_NAME:latest