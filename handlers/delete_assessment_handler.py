import json
from .db_connection import get_db_connection
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_delete_assessment(event, context):
    # Get assessment ID from path
    path = event.get('path', '')
    path = path.lstrip('/')
    path_parts = path.split('/')
    assessment_id = path_parts[2] if len(path_parts) > 2 else None
    logger.info(f"[handle_delete_assessment] Assessment ID: {assessment_id}")

    # Validate that assessment_id is not empty
    if not assessment_id:
        logger.error(f"[handle_delete_assessment] Assessment ID is empty")
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "error": "Invalid assessment ID format"
            })
        }

    try:
        connection = get_db_connection()
        if not connection:
            logger.error(f"[handle_delete_assessment] Failed to connect to database")
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
        
        # First check if the record exists
        check_query = "SELECT id FROM call_sim_scoring WHERE id = %s"
        cursor.execute(check_query, [assessment_id])
        
        if not cursor.fetchone():
            logger.error(f"[handle_delete_assessment] Assessment not found")
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

        # Delete the record
        delete_query = "UPDATE call_sim_scoring SET is_deleted = true WHERE id = %s"
        cursor.execute(delete_query, [assessment_id])
        connection.commit()

        # Return success response
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "message": "Assessment deleted successfully",
                "id": assessment_id
            })
        }
        
    except Exception as e:
        logger.error(f"[handle_delete_assessment] Database error: {e}")
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