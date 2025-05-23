import json
from datetime import datetime
from .db_connection import get_db_connection

def datetime_handler(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def transform_simulation_data(row):
    # Get scores from the accuracy column
    accuracy = row.get('accuracy', {})
    scores = accuracy.get('scores', {})
    
    # Get individual scores
    introduction_score = scores.get('introduction', {}).get('score', 0)
    rapport_score = scores.get('rapport', {}).get('score', 0)
    interest_score = scores.get('creatingInterest', {}).get('score', 0)
    probing_score = scores.get('probing', {}).get('score', 0)
    product_knowledge_score = scores.get('productKnowledge', {}).get('score', 0)
    
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
        "product": row.get('product_id', ''),  # Using product_id since product name isn't available
        "specialty": row.get('specialty', '').capitalize(),
        "overallScore": overall_score,
        "introduction": introduction_score,
        "rapport": rapport_score,
        "interest": interest_score,
        "probing": probing_score,
        "productKnowledge": product_knowledge_score
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