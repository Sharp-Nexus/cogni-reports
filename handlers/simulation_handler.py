import json
import pg8000
import os
from datetime import datetime

def datetime_handler(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def get_db_connection():
    try:
        connection = pg8000.connect(
            host=os.environ.get('DB_HOST'),
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD')
        )
        return connection
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def transform_simulation_data(row):
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
        "userId": row.get('user_id'),
        "date": formatted_date,
        "adoptionLevel": row.get('adoption_continuum', 'naive').capitalize(),
        "situation": row.get('situation', '').capitalize(),
        "product": row.get('product_id', ''),  # Using product_id since product name isn't available
        "specialty": row.get('specialty', '').capitalize(),
        "overallScore": row.get('overall_score', 0),
        "fluency": row.get('fluency', {}).get('scores', {}).get('total', 0),
        "introduction": score_map.get(introduction_score, 0),
        "rapport": score_map.get(rapport_score, 0),
        "interest": score_map.get(interest_score, 0),
        "probing": score_map.get(probing_score, 0),
        "productKnowledge": score_map.get(product_knowledge_score, 0)
    }

def handle_simulation_request(event, context):
    # Get query parameters and path
    query_params = event.get('queryStringParameters', {}) or {}
    path = event.get('path', '')
    
    # Remove leading slash if present
    path = path.lstrip('/')
    
    # Debug logging
    print(f"Simulation handler received path: {path}")
    print(f"Query parameters received: {query_params}")
    
    # Get filters
    product_filter = query_params.get('product')
    specialty_filter = query_params.get('specialty')
    user_id = query_params.get('userId')  # Get user_id from query parameters
    
    print(f"Filters extracted - product: {product_filter}, specialty: {specialty_filter}, userId: {user_id}")
    
    try:
        # Connect to database
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
        if user_id:
            conditions.append("user_id = %s")
            params.append(user_id)
            
        if product_filter and product_filter != 'all':
            conditions.append("product_id = %s")
            params.append(product_filter)
            
        if specialty_filter and specialty_filter != 'all':
            conditions.append("LOWER(specialty) = LOWER(%s)")  # Case-insensitive comparison
            params.append(specialty_filter)
            
        # Combine all conditions with AND
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        print(f"Final SQL query: {query}")
        print(f"Query parameters: {params}")
            
        # Execute query
        cursor.execute(query, params)
        
        # Fetch all results
        columns = [desc[0] for desc in cursor.description]
        results = []
        for row in cursor.fetchall():
            row_dict = dict(zip(columns, row))
            transformed_data = transform_simulation_data(row_dict)
            results.append(transformed_data)
            
        print(f"Number of results found: {len(results)}")
            
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "simulationData": results
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