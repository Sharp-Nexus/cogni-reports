import json

from handlers.benchmarks_handler import handle_benchmarks_request
from handlers.presigned_url_handler import handle_presigned_url_request
from handlers.recommendations_handler import handle_recommendations_request
from handlers.simulation_handler import handle_simulation_request
from handlers.team_members_handler import handle_team_members_request
from handlers.team_overview_handler import handle_team_overview_request
from handlers.sample_data_handler import handle_sample_data_request
from utils.logger import logger

ROUTE_HANDLERS = {
    'simulation-data': handle_simulation_request,
    'team-members': handle_team_members_request,
    'industry-benchmarks': handle_benchmarks_request,
    'team-overview': handle_team_overview_request,
    'insights-recommendations': handle_recommendations_request,
    'presignedPutUrl': handle_presigned_url_request,
    'call-sim-sample-data': handle_sample_data_request,
}

def lambda_handler(event, context):
    path = event.get('path', '')
    http_method = event.get('httpMethod', 'GET')

    logger.info(f"Received request for path: {path}, method: {http_method}")
    logger.info(f"Full event: {json.dumps(event)}")

    path = path.lstrip('/')
    if path.startswith('callsim/'):
        path = path[8:]

    modified_event = event.copy()
    modified_event['path'] = path

    for route_prefix, handler in ROUTE_HANDLERS.items():
        if path.startswith(route_prefix):
            return handler(modified_event, context)

    logger.info(f"No route found for path: {path}, method: {http_method}")
    return {
        "statusCode": 404,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*"
        },
        "body": json.dumps({
            "message": "Route not found",
            "path": path,
            "method": http_method
        })
    }
