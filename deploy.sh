#!/usr/bin/env bash
set -e

echo "Building project with nix..."
nix build

echo "Deploying to AWS Lambda..."
aws lambda update-function-code \
  --function-name arn:aws:lambda:ca-central-1:816069145265:function:CallsimReportsLambda \
  --zip-file fileb://result/dist/lambda.zip \
  --region ca-central-1 \
  --profile SharpNexusDev

echo "Deployment completed successfully!"
