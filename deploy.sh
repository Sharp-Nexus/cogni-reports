#!/usr/bin/env nix-shell
#!nix-shell -i bash -p awscli2 nix-output-monitor
set -e

echo "Building project with nix..."
nom build

echo "Deploying to AWS Lambda..."
aws lambda update-function-code \
  --function-name arn:aws:lambda:ca-central-1:816069145265:function:CallsimReportsLambda \
  --zip-file fileb://result/dist/lambda.zip \
  --region ca-central-1 \
  --profile SharpNexusDev

echo "Deployment completed successfully!"
