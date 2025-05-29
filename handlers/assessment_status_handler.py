import json
from .db_connection import get_db_connection
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_assessment_status(event, context):
    # Get simulation ID from path
    path = event.get('path', '')
    path = path.lstrip('/')
    path_parts = path.split('/')
    simulation_id = path_parts[0] if path_parts else None
    logger.info(f"[handle_assessment_status] Simulation ID: {simulation_id}")

    # Validate that simulation_id is not empty
    if not simulation_id:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "error": "Invalid simulation ID format"
            })
        }

    try:
        connection = get_db_connection()
        if not connection:
            return {
                "statusCode": 500,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*"
                },
                "body": json.dumps({
                    "error": "Failed to connect to database"
                })
            }

        cursor = connection.cursor()
        
        # Query using simulation_id instead of id
        query = "SELECT id, simulation_id, assessment_status FROM call_sim_scoring WHERE simulation_id = %s"
        cursor.execute(query, [simulation_id])
        
        # Fetch the result
        result = cursor.fetchone()
        
        if not result:
            return {
                "statusCode": 404,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*"
                },
                "body": json.dumps({
                    "error": "Assessment not found"
                })
            }

        # Return the status data
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "id": result[0],
                "simulation_id": result[1],
                "status": result[2]
            })
        }
        
    except Exception as e:
        logger.error(f"Database error: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "error": "Database error occurred"
            })
        }
    finally:
        if 'connection' in locals() and connection:
            cursor.close()
            connection.close() 