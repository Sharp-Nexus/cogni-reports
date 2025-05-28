import json
from datetime import datetime
from .db_connection import get_db_connection

def datetime_handler(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def transform_insights_data(row):
    # Get scores from the accuracy column
    accuracy = row.get('accuracy', {})
    scores = accuracy.get('scores', {})
    
    # Get all scores
    introduction_score = scores.get('introduction', {}).get('score', 0)
    rapport_score = scores.get('rapport', {}).get('score', 0)
    interest_score = scores.get('creatingInterest', {}).get('score', 0)
    probing_score = scores.get('probing', {}).get('score', 0)
    product_knowledge_score = scores.get('productKnowledge', {}).get('score', 0)
    overall_score = scores.get('total', {}).get('score', 0)
    
    # Get adoption continuum scores
    adoption_continuum = scores.get('adoptionContinuum', {})
    adoption_continuum_score = adoption_continuum.get('score', 0)
    detailed_scores = adoption_continuum.get('detailed_scores', {})
    strategic_fit = detailed_scores.get('strategic_fit', {}).get('score', 0)
    conversion_momentum = detailed_scores.get('conversion_momentum', {}).get('score', 0)
    
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
        "introduction": introduction_score,
        "rapport": rapport_score,
        "interest": interest_score,
        "probing": probing_score,
        "productKnowledge": product_knowledge_score,
        "strategicFit": strategic_fit,
        "conversionMomentum": conversion_momentum,
        "adoptionContinuumScore": adoption_continuum_score
    }

def calculate_averages(data):
    # Group by adoption level and situation
    adoption_levels = {}
    situations = {}
    
    for item in data:
        # Process adoption levels
        if item['adoptionLevel'] not in adoption_levels:
            adoption_levels[item['adoptionLevel']] = {
                'count': 0,
                'totalScore': 0,
                'totalStrategicFit': 0,
                'totalConversionMomentum': 0
            }
        
        adoption_levels[item['adoptionLevel']]['count'] += 1
        adoption_levels[item['adoptionLevel']]['totalScore'] += item['adoptionContinuumScore']
        adoption_levels[item['adoptionLevel']]['totalStrategicFit'] += item['strategicFit']
        adoption_levels[item['adoptionLevel']]['totalConversionMomentum'] += item['conversionMomentum']
        
        # Process situations
        if item['situation'] not in situations:
            situations[item['situation']] = {
                'count': 0,
                'totalScore': 0
            }
        
        situations[item['situation']]['count'] += 1
        situations[item['situation']]['totalScore'] += item['overallScore']
    
    # Calculate averages
    adoption_data = [
        {
            'name': level,
            'score': data['totalScore'] / data['count'],
            'strategicFit': data['totalStrategicFit'] / data['count'],
            'conversionMomentum': data['totalConversionMomentum'] / data['count']
        }
        for level, data in adoption_levels.items()
    ]
    
    situation_data = [
        {
            'name': situation,
            'score': data['totalScore'] / data['count']
        }
        for situation, data in situations.items()
    ]
    
    return {
        'adoptionData': adoption_data,
        'situationData': situation_data
    }

def handle_simulation_insights(event, context):
    query_params = event.get('queryStringParameters', {}) or {}
    
    # Get filters
    product_filter = query_params.get('product')
    specialty_filter = query_params.get('specialty')
    user_id = query_params.get('userId')
    
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
        if user_id:
            conditions.append("user_id = %s")
            params.append(user_id)
            
        if product_filter and product_filter != 'all':
            conditions.append("product_id = %s")
            params.append(product_filter)
            
        if specialty_filter and specialty_filter != 'all':
            conditions.append("LOWER(specialty) = LOWER(%s)")
            params.append(specialty_filter)
            
        # Combine all conditions with AND
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        # Execute query
        cursor.execute(query, params)
        
        # Fetch all results
        columns = [desc[0] for desc in cursor.description]
        results = []
        for row in cursor.fetchall():
            row_dict = dict(zip(columns, row))
            transformed_data = transform_insights_data(row_dict)
            results.append(transformed_data)
        
        # Calculate averages
        insights_data = calculate_averages(results)
            
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "insightsData": insights_data
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