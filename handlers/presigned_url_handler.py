import json
import boto3
import os

s3_client = boto3.client('s3')

def handle_presigned_url_request(event, context):
    try:
        filename = event['queryStringParameters']['filename']
        bucket_name = os.environ['BUCKET_NAME']
        expiration = 600 # URL valid for 10 mins

        presigned_url = s3_client.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': bucket_name,
                'Key': filename
            },
            ExpiresIn=expiration
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "presignedUrl": presigned_url,
                "accessUrl": "/callsim/" + filename,
            }),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"  # Optional: for CORS
            }
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
