#!/bin/sh

# load env
if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

# login aws ecr
echo "Logging in to AWS ECR at $AWS_ECR in region $AWS_REGION..."
aws --version
aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$AWS_ECR"

# build image
echo "Building Docker image with cache..."
docker pull "$AWS_ECR:latest" || true
docker build --cache-from="$AWS_ECR:latest" -t "$AWS_ECR:latest" .

# push ECR
echo "Pushing Docker image to ECR..."
docker push "$AWS_ECR:latest"

echo "✅ Build and push to ECR completed: $AWS_ECR:latest"