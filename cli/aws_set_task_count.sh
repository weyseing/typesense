#!/bin/bash

REGION="ap-southeast-1"
CLUSTER_ARN="arn:aws:ecs:ap-southeast-1:107698500998:cluster/typesense-poc"
SERVICE_ARN="arn:aws:ecs:ap-southeast-1:107698500998:service/typesense-poc/typesense-poc-service-d3hr8e3a"

# load env
if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

# task count
if [ -z "$1" ]; then
  echo "ERROR: Must enter ECS task count"
  exit 1
fi
TASK_COUNT=$1

# Update ECS task count
aws ecs update-service  \
  --region "$REGION" \
  --cluster "$CLUSTER_ARN" \
  --service "$SERVICE_ARN" \
  --desired-count $TASK_COUNT  | jq 'del(.service.events)'
