import json
from handlers.simulation_handler import handle_simulation_request
from handlers.team_members_handler import handle_team_members_request
from handlers.benchmarks_handler import handle_benchmarks_request
from handlers.team_overview_handler import handle_team_overview_request
from handlers.recommendations_handler import handle_recommendations_request

def lambda_handler(event, context):
    # Get the path from the event
    path = event.get('path', '')
    
    # Debug logging
    print(f"Received request for path: {path}")
    print(f"Full event: {json.dumps(event)}")
    
    # Remove leading slash if present and handle callsim prefix
    path = path.lstrip('/')
    if path.startswith('callsim/'):
        path = path[8:]  # Remove 'callsim/' prefix
    
    # Create a new event with the modified path
    modified_event = event.copy()
    modified_event['path'] = path
    
    # Route the request based on the path
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