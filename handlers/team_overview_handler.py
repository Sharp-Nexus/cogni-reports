import json
from .db_connection import get_db_connection

def calculate_team_averages(cursor, product_id=None, team_id=None):
    """
    Calculate team averages from call_sim_scoring table with optional filters
    """
    # Get available products for this team
    products_query = """
        SELECT DISTINCT product_id 
        FROM call_sim_scoring 
        WHERE team_id::text = %s 
        AND product_id IS NOT NULL
    """
    cursor.execute(products_query, [team_id])
    available_products = [row[0] for row in cursor.fetchall()]

    # Base query
    query = """
        SELECT 
            AVG(overall_score) as overall_avg,
            COUNT(*) as total_simulations,
            AVG(CASE 
                WHEN conversation_data->'analysis'->'evaluation_criteria_results'->'introduction'->>'result' = 'success' THEN 100
                ELSE 0
            END) as introduction_avg,
            AVG(CASE 
                WHEN conversation_data->'analysis'->'evaluation_criteria_results'->'rapport'->>'result' = 'success' THEN 100
                ELSE 0
            END) as rapport_avg,
            AVG(CASE 
                WHEN conversation_data->'analysis'->'evaluation_criteria_results'->'creating_interest'->>'result' = 'success' THEN 100
                ELSE 0
            END) as interest_avg,
            AVG(CASE 
                WHEN conversation_data->'analysis'->'evaluation_criteria_results'->'probing'->>'result' = 'success' THEN 100
                ELSE 0
            END) as probing_avg,
            AVG(CASE 
                WHEN conversation_data->'analysis'->'evaluation_criteria_results'->'product_knowledge'->>'result' = 'success' THEN 100
                ELSE 0
            END) as product_knowledge_avg,
            AVG(CAST(accuracy->'scores'->'total'->>'score' AS FLOAT)) as total_accuracy
        FROM call_sim_scoring
        WHERE 1=1
    """
    params = []

    # Add filters
    if product_id and product_id != 'all':
        query += " AND product_id = %s"
        params.append(product_id)
    
    if team_id and team_id != 'all':
        query += " AND team_id::text = %s"
        params.append(team_id)

    # Execute query
    cursor.execute(query, params)
    result = cursor.fetchone()

    if not result or result[1] == 0:  # Check if no data or zero simulations
        return None

    return {
        "teamAverages": {
            "overall": round(result[0] or 0, 1),  # overall_avg
            "simulations": result[1] or 0,  # total_simulations
            "availableProducts": available_products,  # Add available products to response
            "totalAccuracy": round(result[7] or 0, 1)  # total_accuracy
        }
    }

def calculate_team_comparison(cursor, product_id=None, team_id=None):
    """
    Calculate team comparison data from call_sim_scoring table with optional filters
    """
    # Base query to get team performance metrics with dynamic benchmarks
    query = """
        WITH all_scores AS (
            SELECT 
                CAST(accuracy->'scores'->'introduction'->>'score' AS FLOAT) as intro_score,
                CAST(accuracy->'scores'->'rapport'->>'score' AS FLOAT) as rapport_score,
                CAST(accuracy->'scores'->'creatingInterest'->>'score' AS FLOAT) as interest_score,
                CAST(accuracy->'scores'->'probing'->>'score' AS FLOAT) as probing_score,
                CAST(accuracy->'scores'->'productKnowledge'->>'score' AS FLOAT) as product_score
            FROM call_sim_scoring
            WHERE accuracy IS NOT NULL
        ),
        benchmarks AS (
            SELECT 
                AVG(intro_score) as intro_benchmark,
                AVG(rapport_score) as rapport_benchmark,
                AVG(interest_score) as interest_benchmark,
                AVG(probing_score) as probing_benchmark,
                AVG(product_score) as product_benchmark
            FROM all_scores
        ),
        team_scores AS (
            SELECT 
                CAST(accuracy->'scores'->'introduction'->>'score' AS FLOAT) as intro_score,
                CAST(accuracy->'scores'->'rapport'->>'score' AS FLOAT) as rapport_score,
                CAST(accuracy->'scores'->'creatingInterest'->>'score' AS FLOAT) as interest_score,
                CAST(accuracy->'scores'->'probing'->>'score' AS FLOAT) as probing_score,
                CAST(accuracy->'scores'->'productKnowledge'->>'score' AS FLOAT) as product_score
            FROM call_sim_scoring
            WHERE team_id::text = %s
            {product_filter}
        )
        SELECT 
            'Introduction' as name,
            AVG(intro_score) as team,
            (SELECT intro_benchmark FROM benchmarks) as average
        FROM team_scores
        WHERE intro_score IS NOT NULL
    """

    # Add product filter if specified
    product_filter = ""
    params = [team_id]
    if product_id and product_id != 'all':
        product_filter = "AND product_id = %s"
        params.append(product_id)
    
    query = query.format(product_filter=product_filter)

    # Union with other metrics
    query += """
        UNION ALL
        SELECT 
            'Rapport' as name,
            AVG(rapport_score) as team,
            (SELECT rapport_benchmark FROM benchmarks) as average
        FROM team_scores
        WHERE rapport_score IS NOT NULL
    """

    query += """
        UNION ALL
        SELECT 
            'Creating Interest' as name,
            AVG(interest_score) as team,
            (SELECT interest_benchmark FROM benchmarks) as average
        FROM team_scores
        WHERE interest_score IS NOT NULL
    """

    query += """
        UNION ALL
        SELECT 
            'Probing' as name,
            AVG(probing_score) as team,
            (SELECT probing_benchmark FROM benchmarks) as average
        FROM team_scores
        WHERE probing_score IS NOT NULL
    """

    query += """
        UNION ALL
        SELECT 
            'Product Knowledge' as name,
            AVG(product_score) as team,
            (SELECT product_benchmark FROM benchmarks) as average
        FROM team_scores
        WHERE product_score IS NOT NULL
    """

    # Execute query
    cursor.execute(query, params)
    results = cursor.fetchall()

    if not results or len(results) == 0:
        return None

    # Format results for frontend, converting Decimal to float
    comparison_data = [
        {
            "name": row[0],
            "team": float(round(row[1] or 0, 1)),
            "average": float(row[2])
        }
        for row in results
    ]

    # Check if we have any actual team scores (not just benchmarks)
    has_team_scores = any(data["team"] > 0 for data in comparison_data)
    if not has_team_scores:
        return None

    return {
        "teamComparisonData": comparison_data
    }

def calculate_team_situation(cursor, product_id=None, team_id=None):
    """
    Calculate team performance metrics grouped by situation type
    """
    # Base query to get team performance metrics with dynamic benchmarks
    query = """
        WITH all_scores AS (
            SELECT 
                situation,
                CAST(accuracy->'scores'->'introduction'->>'score' AS FLOAT) as intro_score,
                CAST(accuracy->'scores'->'rapport'->>'score' AS FLOAT) as rapport_score,
                CAST(accuracy->'scores'->'creatingInterest'->>'score' AS FLOAT) as interest_score,
                CAST(accuracy->'scores'->'probing'->>'score' AS FLOAT) as probing_score,
                CAST(accuracy->'scores'->'productKnowledge'->>'score' AS FLOAT) as product_score
            FROM call_sim_scoring
            WHERE accuracy IS NOT NULL
            AND situation IS NOT NULL
        ),
        benchmarks AS (
            SELECT 
                situation,
                AVG(intro_score) as intro_benchmark,
                AVG(rapport_score) as rapport_benchmark,
                AVG(interest_score) as interest_benchmark,
                AVG(probing_score) as probing_benchmark,
                AVG(product_score) as product_benchmark,
                AVG((intro_score + rapport_score + interest_score + probing_score + product_score) / 5) as overall_benchmark
            FROM all_scores
            GROUP BY situation
        ),
        team_scores AS (
            SELECT 
                situation,
                CAST(accuracy->'scores'->'introduction'->>'score' AS FLOAT) as intro_score,
                CAST(accuracy->'scores'->'rapport'->>'score' AS FLOAT) as rapport_score,
                CAST(accuracy->'scores'->'creatingInterest'->>'score' AS FLOAT) as interest_score,
                CAST(accuracy->'scores'->'probing'->>'score' AS FLOAT) as probing_score,
                CAST(accuracy->'scores'->'productKnowledge'->>'score' AS FLOAT) as product_score
            FROM call_sim_scoring
            WHERE team_id::text = %s
            {product_filter}
            AND situation IS NOT NULL
        )
        SELECT 
            t.situation as name,
            AVG((t.intro_score + t.rapport_score + t.interest_score + t.probing_score + t.product_score) / 5) as team,
            b.overall_benchmark as industry
        FROM team_scores t
        JOIN benchmarks b ON t.situation = b.situation
        GROUP BY t.situation, b.overall_benchmark
        ORDER BY t.situation
    """
    
    # Add product filter if specified
    product_filter = ""
    params = [team_id]
    if product_id and product_id != 'all':
        product_filter = "AND product_id = %s"
        params.append(product_id)
    
    query = query.format(product_filter=product_filter)

    # Execute query
    cursor.execute(query, params)
    results = cursor.fetchall()

    if not results:
        return None

    # Format results for frontend, converting Decimal to float
    situation_data = [
        {
            "name": row[0],
            "team": float(round(row[1] or 0, 1)),
            "industry": float(round(row[2] or 0, 1))
        }
        for row in results
    ]

    return {
        "situationData": situation_data
    }

def calculate_team_trend(cursor, product_id=None, team_id=None):
    """
    Calculate team performance trends over time
    """
    # Base query to get team performance metrics with dynamic benchmarks
    query = """
        WITH all_scores AS (
            SELECT 
                DATE_TRUNC('month', created_at) as month,
                CAST(accuracy->'scores'->'introduction'->>'score' AS FLOAT) as intro_score,
                CAST(accuracy->'scores'->'rapport'->>'score' AS FLOAT) as rapport_score,
                CAST(accuracy->'scores'->'creatingInterest'->>'score' AS FLOAT) as interest_score,
                CAST(accuracy->'scores'->'probing'->>'score' AS FLOAT) as probing_score,
                CAST(accuracy->'scores'->'productKnowledge'->>'score' AS FLOAT) as product_score
            FROM call_sim_scoring
            WHERE accuracy IS NOT NULL
            AND created_at >= NOW() - INTERVAL '12 months'
        ),
        benchmarks AS (
            SELECT 
                month,
                AVG(intro_score) as intro_benchmark,
                AVG(rapport_score) as rapport_benchmark,
                AVG(interest_score) as interest_benchmark,
                AVG(probing_score) as probing_benchmark,
                AVG(product_score) as product_benchmark,
                AVG((intro_score + rapport_score + interest_score + probing_score + product_score) / 5) as overall_benchmark
            FROM all_scores
            GROUP BY month
        ),
        team_scores AS (
            SELECT 
                DATE_TRUNC('month', created_at) as month,
                CAST(accuracy->'scores'->'introduction'->>'score' AS FLOAT) as intro_score,
                CAST(accuracy->'scores'->'rapport'->>'score' AS FLOAT) as rapport_score,
                CAST(accuracy->'scores'->'creatingInterest'->>'score' AS FLOAT) as interest_score,
                CAST(accuracy->'scores'->'probing'->>'score' AS FLOAT) as probing_score,
                CAST(accuracy->'scores'->'productKnowledge'->>'score' AS FLOAT) as product_score
            FROM call_sim_scoring
            WHERE team_id::text = %s
            {product_filter}
            AND created_at >= NOW() - INTERVAL '12 months'
        )
        SELECT 
            TO_CHAR(t.month, 'Mon YYYY') as name,
            AVG((t.intro_score + t.rapport_score + t.interest_score + t.probing_score + t.product_score) / 5) as team,
            b.overall_benchmark as industry
        FROM team_scores t
        JOIN benchmarks b ON t.month = b.month
        GROUP BY t.month, b.overall_benchmark
        ORDER BY t.month
    """
    
    # Add product filter if specified
    product_filter = ""
    params = [team_id]
    if product_id and product_id != 'all':
        product_filter = "AND product_id = %s"
        params.append(product_id)
    
    query = query.format(product_filter=product_filter)

    # Execute query
    cursor.execute(query, params)
    results = cursor.fetchall()

    if not results:
        return None

    # Format results for frontend, converting Decimal to float
    trend_data = [
        {
            "name": row[0],
            "team": float(round(row[1] or 0, 1)),
            "industry": float(round(row[2] or 0, 1))
        }
        for row in results
    ]

    return {
        "teamTrendData": trend_data
    }

def calculate_team_adoption(cursor, product_id=None, team_id=None):
    """
    Calculate team performance metrics grouped by adoption level
    """
    # Base query to get team performance metrics with dynamic benchmarks
    query = """
        WITH all_scores AS (
            SELECT 
                adoption_continuum,
                CAST(accuracy->'scores'->'introduction'->>'score' AS FLOAT) as intro_score,
                CAST(accuracy->'scores'->'rapport'->>'score' AS FLOAT) as rapport_score,
                CAST(accuracy->'scores'->'creatingInterest'->>'score' AS FLOAT) as interest_score,
                CAST(accuracy->'scores'->'probing'->>'score' AS FLOAT) as probing_score,
                CAST(accuracy->'scores'->'productKnowledge'->>'score' AS FLOAT) as product_score
            FROM call_sim_scoring
            WHERE accuracy IS NOT NULL
            AND adoption_continuum IS NOT NULL
        ),
        benchmarks AS (
            SELECT 
                adoption_continuum,
                AVG(intro_score) as intro_benchmark,
                AVG(rapport_score) as rapport_benchmark,
                AVG(interest_score) as interest_benchmark,
                AVG(probing_score) as probing_benchmark,
                AVG(product_score) as product_benchmark,
                AVG((intro_score + rapport_score + interest_score + probing_score + product_score) / 5) as overall_benchmark
            FROM all_scores
            GROUP BY adoption_continuum
        ),
        team_scores AS (
            SELECT 
                adoption_continuum,
                CAST(accuracy->'scores'->'introduction'->>'score' AS FLOAT) as intro_score,
                CAST(accuracy->'scores'->'rapport'->>'score' AS FLOAT) as rapport_score,
                CAST(accuracy->'scores'->'creatingInterest'->>'score' AS FLOAT) as interest_score,
                CAST(accuracy->'scores'->'probing'->>'score' AS FLOAT) as probing_score,
                CAST(accuracy->'scores'->'productKnowledge'->>'score' AS FLOAT) as product_score
            FROM call_sim_scoring
            WHERE team_id::text = %s
            {product_filter}
            AND adoption_continuum IS NOT NULL
        )
        SELECT 
            INITCAP(t.adoption_continuum) as name,
            AVG((t.intro_score + t.rapport_score + t.interest_score + t.probing_score + t.product_score) / 5) as team,
            b.overall_benchmark as industry
        FROM team_scores t
        JOIN benchmarks b ON t.adoption_continuum = b.adoption_continuum
        GROUP BY t.adoption_continuum, b.overall_benchmark
        ORDER BY 
            CASE t.adoption_continuum
                WHEN 'naive' THEN 1
                WHEN 'aware' THEN 2
                WHEN 'trialing' THEN 3
                WHEN 'adopter' THEN 4
                WHEN 'advocate' THEN 5
                ELSE 6
            END
    """
    
    # Add product filter if specified
    product_filter = ""
    params = [team_id]
    if product_id and product_id != 'all':
        product_filter = "AND product_id = %s"
        params.append(product_id)
    
    query = query.format(product_filter=product_filter)

    # Execute query
    cursor.execute(query, params)
    results = cursor.fetchall()

    if not results:
        return None

    # Format results for frontend, converting Decimal to float
    adoption_data = [
        {
            "name": row[0],
            "team": float(round(row[1] or 0, 1)),
            "industry": float(round(row[2] or 0, 1))
        }
        for row in results
    ]

    return {
        "adoptionData": adoption_data
    }

def handle_team_overview_request(event, context):
    # Get query parameters
    query_params = event.get('queryStringParameters', {}) or {}
    path = event.get('path', '')
    
    # Remove leading slash if present
    path = path.lstrip('/')
    
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
        
        # Handle different endpoints
        if path == 'team-overview/averages':
            # Get filters from query parameters
            product_id = query_params.get('product')
            team_id = query_params.get('team')
            
            # Calculate averages with filters
            averages_data = calculate_team_averages(cursor, product_id, team_id)
            
            if not averages_data:
                return {
                    "statusCode": 404,
                    "headers": {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": "*",
                        "Access-Control-Allow-Methods": "*"
                    },
                    "body": json.dumps({
                        "error": "No data found for the specified filters"
                    })
                }
            
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*"
                },
                "body": json.dumps(averages_data)
            }
        elif path == 'team-overview/comparison':
            # Get filters from query parameters
            product_id = query_params.get('product')
            team_id = query_params.get('team')
            
            # Calculate comparison data with filters
            comparison_data = calculate_team_comparison(cursor, product_id, team_id)
            
            if not comparison_data:
                return {
                    "statusCode": 404,
                    "headers": {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": "*",
                        "Access-Control-Allow-Methods": "*"
                    },
                    "body": json.dumps({
                        "error": "No data found for the specified filters"
                    })
                }
            
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*"
                },
                "body": json.dumps(comparison_data)
            }
        elif path == 'team-overview/situation':
            # Get filters from query parameters
            product_id = query_params.get('product')
            team_id = query_params.get('team')
            
            # Calculate situation data with filters
            situation_data = calculate_team_situation(cursor, product_id, team_id)
            
            if not situation_data:
                return {
                    "statusCode": 404,
                    "headers": {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": "*",
                        "Access-Control-Allow-Methods": "*"
                    },
                    "body": json.dumps({
                        "error": "No data found for the specified filters"
                    })
                }
            
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*"
                },
                "body": json.dumps(situation_data)
            }
        elif path == 'team-overview/trend':
            # Get filters from query parameters
            product_id = query_params.get('product')
            team_id = query_params.get('team')
            
            # Calculate trend data with filters
            trend_data = calculate_team_trend(cursor, product_id, team_id)
            
            if not trend_data:
                return {
                    "statusCode": 404,
                    "headers": {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": "*",
                        "Access-Control-Allow-Methods": "*"
                    },
                    "body": json.dumps({
                        "error": "No data found for the specified filters"
                    })
                }
            
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*"
                },
                "body": json.dumps(trend_data)
            }
        elif path == 'team-overview/adoption':
            # Get filters from query parameters
            product_id = query_params.get('product')
            team_id = query_params.get('team')
            
            # Calculate adoption data with filters
            adoption_data = calculate_team_adoption(cursor, product_id, team_id)
            
            if not adoption_data:
                return {
                    "statusCode": 404,
                    "headers": {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": "*",
                        "Access-Control-Allow-Methods": "*"
                    },
                    "body": json.dumps({
                        "error": "No data found for the specified filters"
                    })
                }
            
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*"
                },
                "body": json.dumps(adoption_data)
            }
        else:
            # Return error message for unknown paths
            return {
                "statusCode": 404,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*"
                },
                "body": json.dumps({
                    "message": "Route not found",
                    "path": path
                })
            }
            
    except Exception:
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
