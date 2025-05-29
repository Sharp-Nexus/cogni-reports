import json
from datetime import datetime
from .db_connection import get_db_connection

def datetime_handler(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def transform_overview_data(row):
    # Get scores from the accuracy column
    accuracy = row.get('accuracy', {})
    scores = accuracy.get('scores', {})
    
    # Get adoption continuum detailed scores
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
        "strategicFit": strategic_fit,
        "conversionMomentum": conversion_momentum,
        "adoptionContinuumScore": adoption_continuum_score
    }

def transform_adoption_data(row):
    # Get scores from the accuracy column
    accuracy = row.get('accuracy', {})
    scores = accuracy.get('scores', {})
    
    # Get adoption continuum detailed scores
    adoption_continuum = scores.get('adoptionContinuum', {})
    adoption_continuum_score = adoption_continuum.get('score', 0)
    detailed_scores = adoption_continuum.get('detailed_scores', {})
    strategic_fit = detailed_scores.get('strategic_fit', {}).get('score', 0)
    conversion_momentum = detailed_scores.get('conversion_momentum', {}).get('score', 0)
    
    return {
        "name": row.get('adoption_continuum', 'naive').capitalize(),
        "score": adoption_continuum_score,
        "strategicFit": strategic_fit,
        "conversionMomentum": conversion_momentum
    }

def transform_metrics_data(row):
    # Get scores from the accuracy column
    accuracy = row.get('accuracy', {})
    scores = accuracy.get('scores', {})
    
    # Extract all metric scores with null checks
    metrics = {
        'disc': scores.get('disc', {}).get('score', 0) or 0,
        'total': scores.get('total', {}).get('score', 0) or 0,
        'traits': scores.get('traits', {}).get('score', 0) or 0,
        'closing': scores.get('closing', {}).get('score', 0) or 0,
        'probing': scores.get('probing', {}).get('score', 0) or 0,
        'rapport': scores.get('rapport', {}).get('score', 0) or 0,
        'strategy': scores.get('strategy', {}).get('score', 0) or 0,
        'introduction': scores.get('introduction', {}).get('score', 0) or 0,
        'creatingInterest': scores.get('creatingInterest', {}).get('score', 0) or 0,
        'productKnowledge': scores.get('productKnowledge', {}).get('score', 0) or 0,
        'adoptionContinuum': scores.get('adoptionContinuum', {}).get('score', 0) or 0
    }
    
    return metrics

def transform_traits_data(row):
    # Get scores from the accuracy column
    accuracy = row.get('accuracy', {})
    scores = accuracy.get('scores', {})
    traits = scores.get('traits', {})
    detailed_scores = traits.get('detailed_scores', {}).get('traits', {})
    
    # Extract the required trait scores
    return {
        'overall': traits.get('score', 0),
        'clarity': detailed_scores.get('clarity', {}).get('score', 0),
        'confidence': detailed_scores.get('confidence', {}).get('score', 0),
        'empathy': detailed_scores.get('empathy', {}).get('score', 0),
        'engagement': detailed_scores.get('engagement', {}).get('score', 0)
    }

def transform_disc_data(row):
    # Get scores from the accuracy column
    accuracy = row.get('accuracy', {})
    scores = accuracy.get('scores', {})
    disc = scores.get('disc', {})
    detailed_scores = disc.get('detailed_scores', {})
    
    # Extract the required DISC scores
    return {
        'overall': disc.get('score', 0),
        'message_fit': detailed_scores.get('message_fit', {}).get('score', 0),
        'pacing_and_tone': detailed_scores.get('pacing_and_tone', {}).get('score', 0),
        'overall_influence': detailed_scores.get('overall_influence', {}).get('score', 0),
        'objection_handling': detailed_scores.get('objection_handling', {}).get('score', 0),
        'engagement_approach': detailed_scores.get('engagement_approach', {}).get('score', 0)
    }

def handle_simulation_overview(event, context):
    path = event.get('path', '')
    
    # Check if this is a sub-endpoint request
    if path.endswith('/adoption'):
        return handle_simulation_adoption(event, context)
    elif path.endswith('/specialties'):
        return handle_simulation_specialties(event, context)
    elif path.endswith('/accuracy-metrics'):
        return handle_simulation_metrics(event, context)
    elif path.endswith('/traits'):
        return handle_simulation_traits(event, context)
    elif path.endswith('/disc'):
        return handle_simulation_disc(event, context)
    elif path.endswith('/fluency'):
        return handle_simulation_fluency(event, context)
    
    # Default overview endpoint handling
    query_params = event.get('queryStringParameters', {}) or {}
    
    # Get filters
    product_filter = query_params.get('product')
    specialty_filter = query_params.get('specialty')
    mode_filter = query_params.get('mode')
    user_id = query_params.get('userId')
    assessment_status = query_params.get('assessmentStatus')
    
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
            
        if mode_filter and mode_filter != 'all':
            conditions.append("mode = %s")
            params.append(mode_filter)
            
        if assessment_status and assessment_status != 'all':
            conditions.append("assessment_status = %s")
            params.append(assessment_status)
            
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
            transformed_data = transform_overview_data(row_dict)
            results.append(transformed_data)
            
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

def handle_simulation_adoption(event, context):
    query_params = event.get('queryStringParameters', {}) or {}
    
    # Get filters
    product_filter = query_params.get('product')
    specialty_filter = query_params.get('specialty')
    mode_filter = query_params.get('mode')
    user_id = query_params.get('userId')
    assessment_status = query_params.get('assessmentStatus')
    
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
            
        if mode_filter and mode_filter != 'all':
            conditions.append("mode = %s")
            params.append(mode_filter)
            
        if assessment_status and assessment_status != 'all':
            conditions.append("assessment_status = %s")
            params.append(assessment_status)
            
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
            transformed_data = transform_adoption_data(row_dict)
            results.append(transformed_data)
        
        # Calculate averages by adoption level
        adoption_levels = {}
        for item in results:
            level = item['name']
            if level not in adoption_levels:
                adoption_levels[level] = {
                    'count': 0,
                    'totalOverall': 0,
                    'totalStrategicFit': 0,
                    'totalConversionMomentum': 0
                }
            
            adoption_levels[level]['count'] += 1
            adoption_levels[level]['totalOverall'] += item['score']
            adoption_levels[level]['totalStrategicFit'] += item['strategicFit']
            adoption_levels[level]['totalConversionMomentum'] += item['conversionMomentum']
        
        # Calculate final averages
        adoption_data = [
            {
                'name': level,
                'score': data['totalOverall'] / data['count'],
                'strategicFit': data['totalStrategicFit'] / data['count'],
                'conversionMomentum': data['totalConversionMomentum'] / data['count']
            }
            for level, data in adoption_levels.items()
        ]
            
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "adoptionData": adoption_data
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

def handle_simulation_specialties(event, context):
    query_params = event.get('queryStringParameters', {}) or {}
    user_id = query_params.get('userId')
    assessment_status = query_params.get('assessmentStatus')
    
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
        
        # Query to get distinct specialties
        query = "SELECT DISTINCT specialty FROM call_sim_scoring"
        params = []
        conditions = []
        
        if user_id:
            conditions.append("user_id = %s")
            params.append(user_id)
            
        if assessment_status and assessment_status != 'all':
            conditions.append("assessment_status = %s")
            params.append(assessment_status)
            
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        query += " ORDER BY specialty"
        
        # Execute query
        cursor.execute(query, params)
        
        # Fetch all results
        specialties = [row[0].capitalize() for row in cursor.fetchall() if row[0]]
            
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "specialties": specialties
            })
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

def handle_simulation_metrics(event, context):
    query_params = event.get('queryStringParameters', {}) or {}
    
    # Get filters
    product_filter = query_params.get('product')
    specialty_filter = query_params.get('specialty')
    mode_filter = query_params.get('mode')
    user_id = query_params.get('userId')
    assessment_status = query_params.get('assessmentStatus')
    
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
            
        if mode_filter and mode_filter != 'all':
            conditions.append("mode = %s")
            params.append(mode_filter)
            
        if assessment_status and assessment_status != 'all':
            conditions.append("assessment_status = %s")
            params.append(assessment_status)
            
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
            transformed_data = transform_metrics_data(row_dict)
            results.append(transformed_data)
        
        # Calculate averages for each metric
        metric_totals = {}
        count = len(results)
        
        if count > 0:
            for result in results:
                for metric, score in result.items():
                    if metric not in metric_totals:
                        metric_totals[metric] = 0
                    # Ensure score is a number before adding
                    metric_totals[metric] += float(score) if score is not None else 0
            
            # Calculate final averages
            metrics_data = [
                {
                    'name': metric,
                    'score': total / count
                }
                for metric, total in metric_totals.items()
            ]
            
            # Sort by score in descending order
            metrics_data.sort(key=lambda x: x['score'], reverse=True)
        else:
            metrics_data = []
            
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "metricsData": metrics_data
            })
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

def handle_simulation_traits(event, context):
    query_params = event.get('queryStringParameters', {}) or {}
    
    # Get filters
    product_filter = query_params.get('product')
    specialty_filter = query_params.get('specialty')
    mode_filter = query_params.get('mode')
    user_id = query_params.get('userId')
    assessment_status = query_params.get('assessmentStatus')
    
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
            
        if mode_filter and mode_filter != 'all':
            conditions.append("mode = %s")
            params.append(mode_filter)
            
        if assessment_status and assessment_status != 'all':
            conditions.append("assessment_status = %s")
            params.append(assessment_status)
            
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
            transformed_data = transform_traits_data(row_dict)
            results.append(transformed_data)
        
        # Calculate averages for each trait
        trait_totals = {
            'overall': 0,
            'clarity': 0,
            'confidence': 0,
            'empathy': 0,
            'engagement': 0
        }
        count = len(results)
        
        if count > 0:
            for result in results:
                for trait, score in result.items():
                    trait_totals[trait] += score
            
            # Calculate final averages
            traits_data = [
                {
                    'name': trait,
                    'score': total / count
                }
                for trait, total in trait_totals.items()
            ]
            
            # Sort by score in descending order
            traits_data.sort(key=lambda x: x['score'], reverse=True)
        else:
            traits_data = []
            
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "traitsData": traits_data
            })
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

def handle_simulation_disc(event, context):
    query_params = event.get('queryStringParameters', {}) or {}
    
    # Get filters
    product_filter = query_params.get('product')
    specialty_filter = query_params.get('specialty')
    mode_filter = query_params.get('mode')
    user_id = query_params.get('userId')
    assessment_status = query_params.get('assessmentStatus')
    
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
            
        if mode_filter and mode_filter != 'all':
            conditions.append("mode = %s")
            params.append(mode_filter)
            
        if assessment_status and assessment_status != 'all':
            conditions.append("assessment_status = %s")
            params.append(assessment_status)
            
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
            transformed_data = transform_disc_data(row_dict)
            results.append(transformed_data)
        
        # Calculate averages for each DISC component
        disc_totals = {
            'overall': 0,
            'message_fit': 0,
            'pacing_and_tone': 0,
            'overall_influence': 0,
            'objection_handling': 0,
            'engagement_approach': 0
        }
        count = len(results)
        
        if count > 0:
            for result in results:
                for component, score in result.items():
                    disc_totals[component] += score
            
            # Calculate final averages
            disc_data = [
                {
                    'name': component,
                    'score': total / count
                }
                for component, total in disc_totals.items()
            ]
            
            # Sort by score in descending order
            disc_data.sort(key=lambda x: x['score'], reverse=True)
        else:
            disc_data = []
            
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "discData": disc_data
            })
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

def handle_simulation_fluency(event, context):
    query_params = event.get('queryStringParameters', {}) or {}
    
    # Get filters
    product_filter = query_params.get('product')
    specialty_filter = query_params.get('specialty')
    mode_filter = query_params.get('mode')
    user_id = query_params.get('userId')
    assessment_status = query_params.get('assessmentStatus')
    
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
            
        if mode_filter and mode_filter != 'all':
            conditions.append("mode = %s")
            params.append(mode_filter)
            
        if assessment_status and assessment_status != 'all':
            conditions.append("assessment_status = %s")
            params.append(assessment_status)
            
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
            fluency = row_dict.get('fluency', {})
            scores = fluency.get('scores', {})
            
            results.append({
                'wpm': scores.get('wpm', 0),
                'total': scores.get('total', 0),
                'pauses': scores.get('pauses', 0),
                'fillerWords': scores.get('fillerWords', 0)
            })
        
        # Calculate averages for each fluency metric
        fluency_totals = {
            'wpm': 0,
            'total': 0,
            'pauses': 0,
            'fillerWords': 0
        }
        count = len(results)
        
        if count > 0:
            for result in results:
                for metric, score in result.items():
                    fluency_totals[metric] += score
            
            # Calculate final averages
            fluency_data = [
                {
                    'name': metric,
                    'score': total / count
                }
                for metric, total in fluency_totals.items()
            ]
            
            # Sort by score in descending order
            fluency_data.sort(key=lambda x: x['score'], reverse=True)
        else:
            fluency_data = []
            
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "fluencyData": fluency_data
            })
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