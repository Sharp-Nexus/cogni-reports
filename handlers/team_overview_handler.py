import json
from datetime import datetime
from .db_connection import get_db_connection
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_team_averages(cursor, product_id=None, team_id=None, mode=None):
    """
    Calculate team averages from call_sim_scoring table with optional filters
    """
    logger.info(f"Calculating team averages with filters - product_id: {product_id}, team_id: {team_id}, mode: {mode}")
    
    # Get available products for this team
    products_query = """
        SELECT DISTINCT product_id 
        FROM call_sim_scoring 
        WHERE 1=1
    """
    params = []
    
    if team_id and team_id != 'all':
        products_query += " AND team_id::text = %s"
        params.append(team_id)
    
    if mode and mode != 'all':
        products_query += " AND mode = %s"
        params.append(mode)
    
    products_query += " AND product_id IS NOT NULL"
    
    logger.info(f"Executing products query: {products_query}")
    logger.info(f"Products query parameters: {params}")
    
    cursor.execute(products_query, params)
    available_products = [row[0] for row in cursor.fetchall()]
    logger.info(f"Available products: {available_products}")

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

    # Add filters only if they are provided and not 'all'
    if product_id and product_id != 'all':
        query += " AND product_id = %s"
        params.append(product_id)
    
    if team_id and team_id != 'all':
        query += " AND team_id::text = %s"
        params.append(team_id)

    if mode and mode != 'all':
        query += " AND mode = %s"
        params.append(mode)

    logger.info(f"Executing query: {query}")
    logger.info(f"Query parameters: {params}")

    # Execute query
    cursor.execute(query, params)
    result = cursor.fetchone()
    logger.info(f"Query result: {result}")

    if not result or result[1] == 0:  # Check if no data or zero simulations
        logger.info("No data found for the specified filters")
        return None

    response_data = {
        "teamAverages": {
            "overall": round(result[0] or 0, 1),  # overall_avg
            "simulations": result[1] or 0,  # total_simulations
            "availableProducts": available_products,  # Add available products to response
            "totalAccuracy": round(result[7] or 0, 1)  # total_accuracy
        }
    }
    logger.info(f"Response data: {response_data}")
    return response_data

def calculate_team_comparison(cursor, product_id=None, team_id=None, mode=None):
    """
    Calculate team comparison data from call_sim_scoring table with optional filters
    """
    logger.info(f"Calculating team comparison with filters - product_id: {product_id}, team_id: {team_id}, mode: {mode}")
    
    # Base query to get team performance metrics with dynamic benchmarks
    query = """
        WITH team_scores AS (
            SELECT 
                CAST(accuracy->'scores'->'introduction'->>'score' AS FLOAT) as intro_score,
                CAST(accuracy->'scores'->'rapport'->>'score' AS FLOAT) as rapport_score,
                CAST(accuracy->'scores'->'creatingInterest'->>'score' AS FLOAT) as interest_score,
                CAST(accuracy->'scores'->'probing'->>'score' AS FLOAT) as probing_score,
                CAST(accuracy->'scores'->'productKnowledge'->>'score' AS FLOAT) as product_score,
                CAST(accuracy->'scores'->'strategy'->>'score' AS FLOAT) as strategy_score,
                CAST(accuracy->'scores'->'closing'->>'score' AS FLOAT) as closing_score,
                CAST(accuracy->'scores'->'disc'->>'score' AS FLOAT) as disc_score,
                CAST(accuracy->'scores'->'traits'->>'score' AS FLOAT) as traits_score,
                CAST(accuracy->'scores'->'adoptionContinuum'->>'score' AS FLOAT) as adoption_score
            FROM call_sim_scoring
            WHERE accuracy IS NOT NULL
    """
    
    params = []
    if team_id and team_id != 'all':
        query += " AND team_id::text = %s"
        params.append(team_id)
    
    if mode and mode != 'all':
        query += " AND mode = %s"
        params.append(mode)
    
    if product_id and product_id != 'all':
        query += " AND product_id = %s"
        params.append(product_id)
    
    query += """
        )
        SELECT 
            'Introduction' as name,
            AVG(intro_score) as team
        FROM team_scores
        WHERE intro_score IS NOT NULL

        UNION ALL
        SELECT 
            'Rapport' as name,
            AVG(rapport_score) as team
        FROM team_scores
        WHERE rapport_score IS NOT NULL

        UNION ALL
        SELECT 
            'Creating Interest' as name,
            AVG(interest_score) as team
        FROM team_scores
        WHERE interest_score IS NOT NULL

        UNION ALL
        SELECT 
            'Probing' as name,
            AVG(probing_score) as team
        FROM team_scores
        WHERE probing_score IS NOT NULL

        UNION ALL
        SELECT 
            'Product Knowledge' as name,
            AVG(product_score) as team
        FROM team_scores
        WHERE product_score IS NOT NULL

        UNION ALL
        SELECT 
            'Strategy' as name,
            AVG(strategy_score) as team
        FROM team_scores
        WHERE strategy_score IS NOT NULL

        UNION ALL
        SELECT 
            'Closing' as name,
            AVG(closing_score) as team
        FROM team_scores
        WHERE closing_score IS NOT NULL

        UNION ALL
        SELECT 
            'DISC' as name,
            AVG(disc_score) as team
        FROM team_scores
        WHERE disc_score IS NOT NULL

        UNION ALL
        SELECT 
            'Traits' as name,
            AVG(traits_score) as team
        FROM team_scores
        WHERE traits_score IS NOT NULL

        UNION ALL
        SELECT 
            'Adoption Continuum' as name,
            AVG(adoption_score) as team
        FROM team_scores
        WHERE adoption_score IS NOT NULL
    """

    logger.info(f"Executing query: {query}")
    logger.info(f"Query parameters: {params}")

    # Execute query
    cursor.execute(query, params)
    results = cursor.fetchall()
    logger.info(f"Query results: {results}")

    # Format results for frontend, converting Decimal to float
    comparison_data = [
        {
            "name": row[0],
            "team": float(round(row[1] or 0, 1))
        }
        for row in results
    ]

    response_data = {
        "teamComparisonData": comparison_data
    }
    logger.info(f"Response data: {response_data}")
    return response_data

def calculate_team_situation(cursor, product_id=None, team_id=None, mode=None):
    """
    Calculate team performance metrics grouped by situation type
    """
    logger.info(f"Calculating team situation with filters - product_id: {product_id}, team_id: {team_id}, mode: {mode}")
    
    # Base query to get team performance metrics with dynamic benchmarks
    query = """
        WITH team_scores AS (
            SELECT 
                situation,
                CAST(accuracy->'scores'->'introduction'->>'score' AS FLOAT) as intro_score,
                CAST(accuracy->'scores'->'rapport'->>'score' AS FLOAT) as rapport_score,
                CAST(accuracy->'scores'->'creatingInterest'->>'score' AS FLOAT) as interest_score,
                CAST(accuracy->'scores'->'probing'->>'score' AS FLOAT) as probing_score,
                CAST(accuracy->'scores'->'productKnowledge'->>'score' AS FLOAT) as product_score,
                CAST(accuracy->'scores'->'strategy'->>'score' AS FLOAT) as strategy_score,
                CAST(accuracy->'scores'->'closing'->>'score' AS FLOAT) as closing_score,
                CAST(accuracy->'scores'->'disc'->>'score' AS FLOAT) as disc_score,
                CAST(accuracy->'scores'->'traits'->>'score' AS FLOAT) as traits_score,
                CAST(accuracy->'scores'->'adoptionContinuum'->>'score' AS FLOAT) as adoption_score
            FROM call_sim_scoring
            WHERE accuracy IS NOT NULL
            AND situation IS NOT NULL
    """
    
    params = []
    if team_id and team_id != 'all':
        query += " AND team_id::text = %s"
        params.append(team_id)
    
    if mode and mode != 'all':
        query += " AND mode = %s"
        params.append(mode)
    
    if product_id and product_id != 'all':
        query += " AND product_id = %s"
        params.append(product_id)
    
    query += """
        )
        SELECT 
            situation as name,
            AVG((intro_score + rapport_score + interest_score + probing_score + product_score + 
                 strategy_score + closing_score + disc_score + traits_score + adoption_score) / 10) as team
        FROM team_scores
        GROUP BY situation
        ORDER BY situation
    """
    
    logger.info(f"Executing query: {query}")
    logger.info(f"Query parameters: {params}")

    # Execute query
    cursor.execute(query, params)
    results = cursor.fetchall()
    logger.info(f"Query results: {results}")

    # Format results for frontend, converting Decimal to float
    situation_data = [
        {
            "name": row[0],
            "team": float(round(row[1] or 0, 1))
        }
        for row in results
    ]

    response_data = {
        "situationData": situation_data
    }
    logger.info(f"Response data: {response_data}")
    return response_data

def calculate_team_trend(cursor, product_id=None, team_id=None, mode=None):
    """
    Calculate team performance trends over time
    """
    logger.info(f"Calculating team trend with filters - product_id: {product_id}, team_id: {team_id}, mode: {mode}")
    
    # Base query to get team performance metrics with dynamic benchmarks
    query = """
        WITH team_scores AS (
            SELECT 
                DATE_TRUNC('month', created_at) as month,
                CAST(accuracy->'scores'->'introduction'->>'score' AS FLOAT) as intro_score,
                CAST(accuracy->'scores'->'rapport'->>'score' AS FLOAT) as rapport_score,
                CAST(accuracy->'scores'->'creatingInterest'->>'score' AS FLOAT) as interest_score,
                CAST(accuracy->'scores'->'probing'->>'score' AS FLOAT) as probing_score,
                CAST(accuracy->'scores'->'productKnowledge'->>'score' AS FLOAT) as product_score,
                CAST(accuracy->'scores'->'strategy'->>'score' AS FLOAT) as strategy_score,
                CAST(accuracy->'scores'->'closing'->>'score' AS FLOAT) as closing_score,
                CAST(accuracy->'scores'->'disc'->>'score' AS FLOAT) as disc_score,
                CAST(accuracy->'scores'->'traits'->>'score' AS FLOAT) as traits_score,
                CAST(accuracy->'scores'->'adoptionContinuum'->>'score' AS FLOAT) as adoption_score
            FROM call_sim_scoring
            WHERE accuracy IS NOT NULL
            AND created_at >= NOW() - INTERVAL '12 months'
    """
    
    params = []
    if team_id and team_id != 'all':
        query += " AND team_id::text = %s"
        params.append(team_id)
    
    if mode and mode != 'all':
        query += " AND mode = %s"
        params.append(mode)
    
    if product_id and product_id != 'all':
        query += " AND product_id = %s"
        params.append(product_id)
    
    query += """
        )
        SELECT 
            TO_CHAR(month, 'Mon YYYY') as name,
            AVG((intro_score + rapport_score + interest_score + probing_score + product_score + 
                 strategy_score + closing_score + disc_score + traits_score + adoption_score) / 10) as team
        FROM team_scores
        GROUP BY month
        ORDER BY month
    """
    
    logger.info(f"Executing query: {query}")
    logger.info(f"Query parameters: {params}")

    # Execute query
    cursor.execute(query, params)
    results = cursor.fetchall()
    logger.info(f"Query results: {results}")

    # Format results for frontend, converting Decimal to float
    trend_data = [
        {
            "name": row[0],
            "team": float(round(row[1] or 0, 1))
        }
        for row in results
    ]

    response_data = {
        "teamTrendData": trend_data
    }
    logger.info(f"Response data: {response_data}")
    return response_data

def calculate_team_adoption(cursor, product_id=None, team_id=None, mode=None):
    """
    Calculate team performance metrics grouped by adoption level
    """
    logger.info(f"Calculating team adoption with filters - product_id: {product_id}, team_id: {team_id}, mode: {mode}")
    
    # Base query to get team performance metrics with dynamic benchmarks
    query = """
        WITH team_scores AS (
            SELECT 
                adoption_continuum,
                CAST(accuracy->'scores'->'introduction'->>'score' AS FLOAT) as intro_score,
                CAST(accuracy->'scores'->'rapport'->>'score' AS FLOAT) as rapport_score,
                CAST(accuracy->'scores'->'creatingInterest'->>'score' AS FLOAT) as interest_score,
                CAST(accuracy->'scores'->'probing'->>'score' AS FLOAT) as probing_score,
                CAST(accuracy->'scores'->'productKnowledge'->>'score' AS FLOAT) as product_score,
                CAST(accuracy->'scores'->'strategy'->>'score' AS FLOAT) as strategy_score,
                CAST(accuracy->'scores'->'closing'->>'score' AS FLOAT) as closing_score,
                CAST(accuracy->'scores'->'disc'->>'score' AS FLOAT) as disc_score,
                CAST(accuracy->'scores'->'traits'->>'score' AS FLOAT) as traits_score,
                CAST(accuracy->'scores'->'adoptionContinuum'->>'score' AS FLOAT) as adoption_score
            FROM call_sim_scoring
            WHERE accuracy IS NOT NULL
            AND adoption_continuum IS NOT NULL
    """
    
    params = []
    if team_id and team_id != 'all':
        query += " AND team_id::text = %s"
        params.append(team_id)
    
    if mode and mode != 'all':
        query += " AND mode = %s"
        params.append(mode)
    
    if product_id and product_id != 'all':
        query += " AND product_id = %s"
        params.append(product_id)
    
    query += """
        )
        SELECT 
            INITCAP(adoption_continuum) as name,
            AVG((intro_score + rapport_score + interest_score + probing_score + product_score + 
                 strategy_score + closing_score + disc_score + traits_score + adoption_score) / 10) as team
        FROM team_scores
        GROUP BY adoption_continuum
        ORDER BY 
            CASE adoption_continuum
                WHEN 'naive' THEN 1
                WHEN 'aware' THEN 2
                WHEN 'trialing' THEN 3
                WHEN 'adopter' THEN 4
                WHEN 'advocate' THEN 5
                ELSE 6
            END
    """
    
    logger.info(f"Executing query: {query}")
    logger.info(f"Query parameters: {params}")

    # Execute query
    cursor.execute(query, params)
    results = cursor.fetchall()
    logger.info(f"Query results: {results}")

    # Format results for frontend, converting Decimal to float
    adoption_data = [
        {
            "name": row[0],
            "team": float(round(row[1] or 0, 1))
        }
        for row in results
    ]

    response_data = {
        "adoptionData": adoption_data
    }
    logger.info(f"Response data: {response_data}")
    return response_data

def calculate_team_accuracy(cursor, product_id=None, team_id=None, mode=None):
    """
    Calculate team accuracy metrics from call_sim_scoring table
    """
    logger.info(f"Calculating team accuracy with filters - product_id: {product_id}, team_id: {team_id}, mode: {mode}")
    
    # Base query
    query = """
        SELECT 
            AVG(CAST(accuracy->'scores'->'total'->>'score' AS FLOAT)) as total_accuracy
        FROM call_sim_scoring
        WHERE 1=1
    """
    
    # Build parameters list
    params = []
    
    # Add filters only if they are provided and not 'all'
    if team_id and team_id != 'all':
        query += " AND team_id::text = %s"
        params.append(team_id)
    
    if product_id and product_id != 'all':
        query += " AND product_id = %s"
        params.append(product_id)
    
    if mode and mode != 'all':
        query += " AND mode = %s"
        params.append(mode)

    logger.info(f"Executing query: {query}")
    logger.info(f"Query parameters: {params}")

    cursor.execute(query, params)
    result = cursor.fetchone()
    logger.info(f"Query result: {result}")

    response_data = {
        "accuracyData": {
            "totalAccuracy": round(result[0] if result and result[0] is not None else 0, 1)
        }
    }
    logger.info(f"Response data: {response_data}")
    return response_data

def calculate_team_fluency(cursor, product_id=None, team_id=None, mode=None):
    """
    Calculate team fluency metrics from call_sim_scoring table
    """
    logger.info(f"Calculating team fluency with filters - product_id: {product_id}, team_id: {team_id}, mode: {mode}")
    
    # Base query
    query = """
        SELECT 
            AVG(CAST(fluency->'scores'->'wpm' AS FLOAT)) as wpm,
            AVG(CAST(fluency->'scores'->'total' AS FLOAT)) as total,
            AVG(CAST(fluency->'scores'->'pauses' AS FLOAT)) as pauses,
            AVG(CAST(fluency->'scores'->'fillerWords' AS FLOAT)) as filler_words
        FROM call_sim_scoring
        WHERE fluency IS NOT NULL
    """
    
    # Build parameters list
    params = []
    
    # Add filters only if they are provided and not 'all'
    if team_id and team_id != 'all':
        query += " AND team_id::text = %s"
        params.append(team_id)
    
    if product_id and product_id != 'all':
        query += " AND product_id = %s"
        params.append(product_id)
    
    if mode and mode != 'all':
        query += " AND mode = %s"
        params.append(mode)

    logger.info(f"Executing query: {query}")
    logger.info(f"Query parameters: {params}")

    cursor.execute(query, params)
    result = cursor.fetchone()
    logger.info(f"Query result: {result}")

    response_data = {
        "fluencyData": {
            "wpm": round(result[0] if result and result[0] is not None else 0, 1),
            "total": round(result[1] if result and result[1] is not None else 0, 1),
            "pauses": round(result[2] if result and result[2] is not None else 0, 1),
            "fillerWords": round(result[3] if result and result[3] is not None else 0, 1)
        }
    }
    logger.info(f"Response data: {response_data}")
    return response_data

def calculate_team_simulation_count(cursor, product_id=None, team_id=None, mode=None):
    """
    Calculate total number of simulations for the team
    """
    logger.info(f"Calculating team simulation count with filters - product_id: {product_id}, team_id: {team_id}, mode: {mode}")
    
    # Base query
    query = """
        SELECT COUNT(*) as total_simulations
        FROM call_sim_scoring
        WHERE 1=1
    """
    
    # Build parameters list
    params = []
    
    # Add filters only if they are provided and not 'all'
    if team_id and team_id != 'all':
        query += " AND team_id::text = %s"
        params.append(team_id)
    
    if product_id and product_id != 'all':
        query += " AND product_id = %s"
        params.append(product_id)
    
    if mode and mode != 'all':
        query += " AND mode = %s"
        params.append(mode)

    logger.info(f"Executing query: {query}")
    logger.info(f"Query parameters: {params}")

    cursor.execute(query, params)
    result = cursor.fetchone()
    logger.info(f"Query result: {result}")

    response_data = {
        "simulationCount": {
            "total": result[0] if result and result[0] is not None else 0
        }
    }
    logger.info(f"Response data: {response_data}")
    return response_data

def handle_team_overview_request(event, context):
    # Get query parameters
    query_params = event.get('queryStringParameters', {}) or {}
    path = event.get('path', '')
    
    # Remove leading slash if present
    path = path.lstrip('/')
    
    logger.info(f"Handling request for path: {path}")
    logger.info(f"Query parameters: {query_params}")
    
    try:
        # Connect to database
        connection = get_db_connection()
        if not connection:
            logger.error("Failed to connect to database")
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
        
        # Get filters from query parameters
        product_id = query_params.get('product')
        team_id = query_params.get('team')
        mode = query_params.get('mode')
        
        logger.info(f"Processing request with filters - product_id: {product_id}, team_id: {team_id}, mode: {mode}")

        # Handle different endpoints
        if path == 'team-overview/averages':
            averages_data = calculate_team_averages(cursor, product_id, team_id, mode)
            if not averages_data:
                logger.info("No averages data found")
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
        elif path == 'team-overview/accuracy':
            accuracy_data = calculate_team_accuracy(cursor, product_id, team_id, mode)
            if not accuracy_data:
                logger.info("No accuracy data found")
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
                "body": json.dumps(accuracy_data)
            }
        elif path == 'team-overview/fluency':
            fluency_data = calculate_team_fluency(cursor, product_id, team_id, mode)
            if not fluency_data:
                logger.info("No fluency data found")
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
                "body": json.dumps(fluency_data)
            }
        elif path == 'team-overview/simulation-count':
            count_data = calculate_team_simulation_count(cursor, product_id, team_id, mode)
            if not count_data:
                logger.info("No simulation count data found")
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
                "body": json.dumps(count_data)
            }
        elif path == 'team-overview/comparison':
            comparison_data = calculate_team_comparison(cursor, product_id, team_id, mode)
            if not comparison_data:
                logger.info("No comparison data found")
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
            situation_data = calculate_team_situation(cursor, product_id, team_id, mode)
            if not situation_data:
                logger.info("No situation data found")
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
            trend_data = calculate_team_trend(cursor, product_id, team_id, mode)
            if not trend_data:
                logger.info("No trend data found")
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
            adoption_data = calculate_team_adoption(cursor, product_id, team_id, mode)
            if not adoption_data:
                logger.info("No adoption data found")
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
            logger.info(f"Unknown path requested: {path}")
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
            
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
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