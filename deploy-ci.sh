#!/usr/bin/env nix-shell
#!nix-shell -i bash -p awscli2
set -e

echo "Deploying to AWS Lambda..."
aws lambda update-function-code \
  --function-name "${AWS_LAMBDA_ARN}" \
  --zip-file fileb://result/dist/lambda.zip \
  --region "${AWS_REGION}"

echo "Deployment completed successfully!"
