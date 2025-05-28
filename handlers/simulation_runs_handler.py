import json
from datetime import datetime
from .db_connection import get_db_connection

def datetime_handler(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def transform_simulation_run_data(row):
    # Get scores from the accuracy column
    accuracy = row.get('accuracy', {})
    scores = accuracy.get('scores', {})
    
    # Get individual scores
    introduction_score = scores.get('introduction', {}).get('score', 0)
    rapport_score = scores.get('rapport', {}).get('score', 0)
    interest_score = scores.get('creatingInterest', {}).get('score', 0)
    probing_score = scores.get('probing', {}).get('score', 0)
    product_knowledge_score = scores.get('productKnowledge', {}).get('score', 0)
    strategy_score = scores.get('strategy', {}).get('score', 0)
    closing_score = scores.get('closing', {}).get('score', 0)
    
    # Get DISC data with feedback
    disc_data = scores.get('disc', {})
    disc_score = disc_data.get('score', 0)
    disc_feedback = disc_data.get('feedback', '')
    
    # Get traits data with feedback
    traits_data = scores.get('traits', {})
    traits_score = traits_data.get('score', 0)
    traits_feedback = traits_data.get('feedback', '')
    
    # Get adoption continuum data with feedback
    adoption_data = scores.get('adoptionContinuum', {})
    adoption_score = adoption_data.get('score', 0)
    adoption_feedback = adoption_data.get('feedback', '')
    
    # Get overall score from scores.total.score
    overall_score = scores.get('total', {}).get('score', 0)
    
    # Handle date formatting
    created_at = row.get('created_at')
    if isinstance(created_at, datetime):
        formatted_date = created_at.strftime('%B %d, %Y')
    else:
        formatted_date = datetime.now().strftime('%B %d, %Y')
    
    return {
        "id": row.get('id'),
        "userId": row.get('user_id'),
        "date": formatted_date,
        "adoptionLevel": row.get('adoption_continuum', 'naive').capitalize(),
        "situation": row.get('situation', '').capitalize(),
        "product": row.get('product_id', ''),
        "specialty": row.get('specialty', '').capitalize(),
        "overallScore": overall_score,
        "metrics": {
            "introduction": {
                "score": introduction_score
            },
            "rapport": {
                "score": rapport_score
            },
            "creatingInterest": {
                "score": interest_score
            },
            "probing": {
                "score": probing_score
            },
            "productKnowledge": {
                "score": product_knowledge_score
            },
            "strategy": {
                "score": strategy_score
            },
            "closing": {
                "score": closing_score
            },
            "disc": {
                "score": disc_score,
                "feedback": disc_feedback
            },
            "traits": {
                "score": traits_score,
                "feedback": traits_feedback
            },
            "adoptionContinuum": {
                "score": adoption_score,
                "feedback": adoption_feedback
            }
        }
    }

def handle_simulation_run(event, context):
    query_params = event.get('queryStringParameters', {}) or {}
    path = event.get('path', '')
    path = path.lstrip('/')
    
    # Get simulation ID from path
    # The path will be like /simulation-run/{id}
    path_parts = path.split('/')
    simulation_id = path_parts[-1] if len(path_parts) > 1 else None
    
    # Validate that simulation_id is a valid integer
    if simulation_id and not simulation_id.isdigit():
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
        
        # Base query
        query = "SELECT * FROM call_sim_scoring"
        params = []
        conditions = []
        
        # Add filters
        if simulation_id:
            conditions.append("id = %s")
            params.append(int(simulation_id))
        else:
            # Add other filters like in overview handler
            user_id = query_params.get('userId')
            product_filter = query_params.get('product')
            specialty_filter = query_params.get('specialty')
            mode_filter = query_params.get('mode')
            
            if user_id:
                conditions.append("user_id = %s")
                params.append(user_id)
                
            if product_filter and product_filter != 'all':
                conditions.append("product_id = %s")
                params.append(product_filter)
                
            if specialty_filter and specialty_filter != 'all':
                conditions.append("LOWER(specialty) = LOWER(%s)")
                params.append(specialty_filter)
                
            if mode_filter and mode_filter != 'all':
                conditions.append("mode = %s")
                params.append(mode_filter)
            
        # Combine all conditions with AND
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        # Add ordering by date
        query += " ORDER BY created_at DESC"
            
        # Execute query
        cursor.execute(query, params)
        
        # Fetch all results
        columns = [desc[0] for desc in cursor.description]
        results = []
        for row in cursor.fetchall():
            row_dict = dict(zip(columns, row))
            transformed_data = transform_simulation_run_data(row_dict)
            results.append(transformed_data)
        
        # Return empty array if no results found, instead of 404 error
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "simulationData": results if not simulation_id else results[0] if results else []
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