import json
import simulation_data
def lambda_handler(event, context):
    print(f"Event: {json.dumps(event, indent=4)}\n")
    proxy = event["proxy"] || None
    match proxy:
        case "simulation_data":
            return simulation_data.lambda_handler(event, context)
        case _:
            return {
                "statusCode": 404,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*"
                },
                "body": "Not found",
            }
