import json

from handlers.benchmarks_handler import handle_benchmarks_request
from handlers.presigned_url_handler import handle_presigned_url_request
from handlers.recommendations_handler import handle_recommendations_request
from handlers.simulation_overview_handler import handle_simulation_overview
from handlers.simulation_runs_handler import handle_simulation_run
from handlers.simulation_insights_handler import handle_simulation_insights
from handlers.team_members_handler import handle_team_members_request
from handlers.team_overview_handler import handle_team_overview_request
from handlers.sample_data_handler import handle_sample_data_request
from handlers.assessment_status_handler import handle_assessment_status
from handlers.delete_assessment_handler import handle_delete_assessment
from utils.logger import logger

ROUTE_HANDLERS = {
    'GET:simulation-insights': handle_simulation_insights,
    'GET:simulation-run': handle_simulation_run,
    'GET:simulation-overview': handle_simulation_overview,
    'GET:team-members': handle_team_members_request,
    'GET:industry-benchmarks': handle_benchmarks_request,
    'GET:team-overview': handle_team_overview_request,
    'GET:insights-recommendations': handle_recommendations_request,
    'GET:presignedPutUrl': handle_presigned_url_request,
    'GET:call-sim-sample-data': handle_sample_data_request,
}

def lambda_handler(event, context):
    path = event.get('path', '')
    http_method = event.get('httpMethod', 'GET')

    logger.info(f"Received request for path: {path}, method: {http_method}")
    logger.info(f"Full event: {json.dumps(event)}")

    path = path.lstrip('/')
    if path.startswith('callsim/'):
        path = path[8:]
        # Path format for handle_assessment_status: "callsim/<assessment-id>/status"
        path_parts = path.split('/')
        if len(path_parts) == 2 and path_parts[1] == 'status':
            return handle_assessment_status(event, context)
        # Path format for delete: "callsim/id/<id>"
        elif http_method == 'DELETE' and len(path_parts) == 2 and path_parts[0] == 'id':
            return handle_delete_assessment(event, context)

    modified_event = event.copy()
    modified_event['path'] = path

    for route_prefix, handler in ROUTE_HANDLERS.items():
        methodAndPath = f'{http_method}:{path}'
        logger.info(f"[lambda_handler] +++++++ path: {path} http_method: {http_method} route_prefix: {route_prefix} methodAndPath: {methodAndPath}")
        if methodAndPath.startswith(route_prefix):
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
