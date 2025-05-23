import json
from handlers.benchmarks_handler import handle_benchmarks_request
from handlers.presigned_url_handler import handle_presigned_url_request
from handlers.recommendations_handler import handle_recommendations_request
from handlers.simulation_handler import handle_simulation_request
from handlers.team_members_handler import handle_team_members_request
from handlers.team_overview_handler import handle_team_overview_request
from handlers.sample_data_handler import handle_sample_data_request

def lambda_handler(event, context):
    path = event.get('path', '')

    print(f"Received request for path: {path}")
    print(f"Full event: {json.dumps(event)}")

    path = path.lstrip('/')
    if path.startswith('callsim/'):
        path = path[8:]

    modified_event = event.copy()
    modified_event['path'] = path
    
    # Consider using switch statement
    if path.startswith('simulation-data'):
        return handle_simulation_request(modified_event, context)
    elif path.startswith('team-members'):
        return handle_team_members_request(modified_event, context)
    elif path.startswith('industry-benchmarks'):
        return handle_benchmarks_request(modified_event, context)
    elif path.startswith('team-overview'):
        return handle_team_overview_request(modified_event, context)
    elif path.startswith('insights-recommendations'):
        return handle_recommendations_request(modified_event, context)
    elif path.startswith('presignedPutUrl'):
        return handle_presigned_url_request(modified_event, context)
    elif path.startswith('call-sim-sample-data'):
        return handle_sample_data_request(modified_event, context)
    else:
        print(f"No route found for path: {path}")
        return {
            "statusCode": 404,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "message": "Route not found",
                "path": path
            })
        } 
