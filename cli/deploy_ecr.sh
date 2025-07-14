#!/bin/sh

# check env
if [ -z "$AWS_REGION" ] || [ -z "$AWS_ECR" ]; then
  echo "Error: AWS_REGION and AWS_ECR env variables are NOT set."
  exit 1
fi

# login aws ecr
echo "Logging in to AWS ECR at $AWS_ECR in region $AWS_REGION..."
aws --version
aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$AWS_ECR"