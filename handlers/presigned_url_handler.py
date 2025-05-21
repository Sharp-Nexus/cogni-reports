import json
import boto3
import os

s3_client = boto3.client('s3')

def handle_presigned_url_request(event, context):
    try:
        key = event['queryStringParameters']['filename']
        bucket_name = os.environ['BUCKET_NAME']
        expiration = 600 # URL valid for 10 mins

        presigned_url = s3_client.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': bucket_name,
                'Key': key,
                'Metadata': {
                    'x-amz-meta-simulationId': event['queryStringParameters']['simulationId'],
                    'x-amz-meta-productId': event['queryStringParameters']['productId'],
                    'x-amz-meta-materialId': event['queryStringParameters']['materialId'],
                    'x-amz-meta-userId': event['queryStringParameters']['userId'],
                    'x-amz-meta-teamId': event['queryStringParameters']['teamId'],
                    'x-amz-meta-language': event['queryStringParameters']['language'],
                    'x-amz-meta-character': event['queryStringParameters']['character'],
                    'x-amz-meta-specialty': event['queryStringParameters']['specialty'],
                    'x-amz-meta-adoptionContinuum': event['queryStringParameters']['adoptionContinuum'],
                    'x-amz-meta-temperament': event['queryStringParameters']['temperament'],
                    'x-amz-meta-situation': event['queryStringParameters']['situation'],
                    'x-amz-meta-agent': event['queryStringParameters']['agent'],
                    'x-amz-meta-disc': event['queryStringParameters']['disc']
                }
            },
            ExpiresIn=expiration
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "presignedUrl": presigned_url,
                "accessUrl": "/callsim/" + key,
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
