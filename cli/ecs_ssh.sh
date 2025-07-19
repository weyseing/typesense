#!/bin/bash

REGION="ap-southeast-1"
CLUSTER_ARN="arn:aws:ecs:ap-southeast-1:107698500998:cluster/typesense"

# load env
if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi

# task ID
if [ -z "$1" ]; then
  echo "ERROR: Must enter ECS task ID"
  exit 1
fi
TASK_ID=$1

# exec
aws ecs execute-command \
  --region "$REGION" \
  --cluster "$CLUSTER_ARN" \
  --task "$TASK_ID" \
  --command "/bin/bash" \
  --interactive