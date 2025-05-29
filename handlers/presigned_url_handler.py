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
                'Metadata':{
                    'simulationId': event['queryStringParameters']['simulationId'],
                    'productId': event['queryStringParameters']['productId'],
                    'materialId': event['queryStringParameters']['materialId'],
                    'userId': event['queryStringParameters']['userId'],
                    'teamId': event['queryStringParameters']['teamId'],
                    'language': event['queryStringParameters']['language'],
                    'character': event['queryStringParameters']['character'],
                    'specialty': event['queryStringParameters']['specialty'],
                    'adoptionContinuum': event['queryStringParameters']['adoptionContinuum'],
                    'temperament': event['queryStringParameters']['temperament'],
                    'situation': event['queryStringParameters']['situation'],
                    'agent': event['queryStringParameters']['agent'],
                    'disc': event['queryStringParameters']['disc'],
                    'mode': event['queryStringParameters']['mode'],
                    'recordVideo': str(event['queryStringParameters']['recordVideo'])
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
