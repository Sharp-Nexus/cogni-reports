import json
from datetime import datetime
from .db_connection import get_db_connection
from .simulation_handler import datetime_handler

def transform_sample_data(row):
    # Extract data from the conversation_data
    conversation_data = row.get('conversation_data', {})
    analysis = conversation_data.get('analysis', {})
    evaluation_results = analysis.get('evaluation_criteria_results', {})
    
    # Get scores from evaluation results
    introduction_score = evaluation_results.get('introduction', {}).get('result', 'failure')
    rapport_score = evaluation_results.get('rapport', {}).get('result', 'failure')
    interest_score = evaluation_results.get('creating_interest', {}).get('result', 'failure')
    probing_score = evaluation_results.get('probing', {}).get('result', 'failure')
    product_knowledge_score = evaluation_results.get('product_knowledge', {}).get('result', 'failure')
    
    # Convert scores to numeric values
    score_map = {'success': 100, 'failure': 0}
    
    # Handle date formatting
    created_at = row.get('created_at')
    if isinstance(created_at, datetime):
        formatted_date = created_at.strftime('%B %d, %Y')
    else:
        formatted_date = datetime.now().strftime('%B %d, %Y')
    
    return {
        "id": row.get('id'),
        "simulationId": row.get('simulation_id'),
        "productId": row.get('product_id'),
        "materialId": row.get('material_id'),
        "userId": row.get('user_id'),
        "teamId": row.get('team_id'),
        "language": row.get('language'),
        "character": row.get('character'),
        "specialty": row.get('specialty', '').capitalize(),
        "adoptionLevel": row.get('adoption_continuum', 'naive').capitalize(),
        "temperament": row.get('temperament'),
        "situation": row.get('situation', '').capitalize(),
        "agent": row.get('agent'),
        "disc": row.get('disc'),
        "conversationId": row.get('conversation_id'),
        "conversationData": row.get('conversation_data'),
        "videoDurationInSeconds": row.get('video_duration_in_seconds'),
        "transcript": row.get('transcript'),
        "speakerKey": row.get('speaker_key'),
        "fluency": row.get('fluency'),
        "accuracy": row.get('accuracy'),
        "overallScore": row.get('overall_score', 0),
        "createdAt": row.get('created_at'),
        "updatedAt": row.get('updated_at'),
        # Additional computed fields
        "date": formatted_date,
        "introduction": score_map.get(introduction_score, 0),
        "rapport": score_map.get(rapport_score, 0),
        "interest": score_map.get(interest_score, 0),
        "probing": score_map.get(probing_score, 0),
        "productKnowledge": score_map.get(product_knowledge_score, 0)
    }

def handle_sample_data_request(event, context):
    """
    Handler for retrieving a single sample record from call_sim_scoring table.
    Returns a 200 status code with the sample data or appropriate error response.
    """
    try:
        # Connect to database using the shared connection function
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
        
        # Query to get one random record from call_sim_scoring
        query = "SELECT * FROM call_sim_scoring ORDER BY RANDOM() LIMIT 1"
        
        # Execute query
        cursor.execute(query)
        
        # Fetch the result
        columns = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()
        
        if not row:
            return {
                "statusCode": 404,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*"
                },
                "body": json.dumps({
                    "error": "No sample data found"
                })
            }
            
        # Transform the data using our new transformation function
        row_dict = dict(zip(columns, row))
        transformed_data = transform_sample_data(row_dict)
            
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "sampleData": transformed_data
            }, default=datetime_handler)
        }
        
    except Exception as e:
        print(f"Database error: {e}")
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