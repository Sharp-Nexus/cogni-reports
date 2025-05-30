import json
from .db_connection import get_db_connection

def calculate_skill_data(cursor, product_id=None, team_id=None):
    """
    Calculate skill comparison data from call_sim_scoring table
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
            AND team_id::text != %s
        ),
        benchmarks AS (
            SELECT 
                AVG(intro_score) as intro_benchmark,
                AVG(rapport_score) as rapport_benchmark,
                AVG(interest_score) as interest_benchmark,
                AVG(probing_score) as probing_benchmark,
                AVG(product_score) as product_benchmark,
                AVG((intro_score + rapport_score + interest_score + probing_score + product_score) / 5) as total_benchmark
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
        SELECT * FROM (
            SELECT 
                'Overall Score' as subject,
                AVG((intro_score + rapport_score + interest_score + probing_score + product_score) / 5) as team_avg,
                (SELECT total_benchmark FROM benchmarks) as benchmark
            FROM team_scores
            WHERE intro_score IS NOT NULL 
            AND rapport_score IS NOT NULL 
            AND interest_score IS NOT NULL 
            AND probing_score IS NOT NULL 
            AND product_score IS NOT NULL
            UNION ALL
            SELECT 
                'Introduction' as subject,
                AVG(intro_score) as team_avg,
                (SELECT intro_benchmark FROM benchmarks) as benchmark
            FROM team_scores
            WHERE intro_score IS NOT NULL
            UNION ALL
            SELECT 
                'Rapport' as subject,
                AVG(rapport_score) as team_avg,
                (SELECT rapport_benchmark FROM benchmarks) as benchmark
            FROM team_scores
            WHERE rapport_score IS NOT NULL
            UNION ALL
            SELECT 
                'Interest' as subject,
                AVG(interest_score) as team_avg,
                (SELECT interest_benchmark FROM benchmarks) as benchmark
            FROM team_scores
            WHERE interest_score IS NOT NULL
            UNION ALL
            SELECT 
                'Probing' as subject,
                AVG(probing_score) as team_avg,
                (SELECT probing_benchmark FROM benchmarks) as benchmark
            FROM team_scores
            WHERE probing_score IS NOT NULL
            UNION ALL
            SELECT 
                'Product' as subject,
                AVG(product_score) as team_avg,
                (SELECT product_benchmark FROM benchmarks) as benchmark
            FROM team_scores
            WHERE product_score IS NOT NULL
        ) sub
        WHERE team_avg IS NOT NULL
    """
    
    # Add product filter if specified
    product_filter = ""
    params = [team_id, team_id]  # team_id is used twice - once for excluding from benchmark, once for team scores
    if product_id and product_id != 'all':
        product_filter = "AND product_id = %s"
        params.append(product_id)
    
    query = query.format(product_filter=product_filter)

    # Execute query
    cursor.execute(query, params)
    results = cursor.fetchall()

    if not results:
        return []  # Return empty array if no data

    # Format results for frontend
    skill_data = [
        {
            "subject": row[0],
            "teamAvg": float(round(row[1] or 0, 1)),
            "benchmark": float(round(row[2] or 0, 1))
        }
        for row in results
    ]

    return skill_data

def calculate_benchmark_data(cursor, product_id=None, team_id=None):
    """
    Calculate benchmark comparison data from call_sim_scoring table
    """
    # Base query to get team performance metrics with dynamic benchmarks
    query = """
        WITH all_scores AS (
            SELECT 
                team_id,
                AVG(CAST(accuracy->'scores'->'introduction'->>'score' AS FLOAT)) as intro_score,
                AVG(CAST(accuracy->'scores'->'rapport'->>'score' AS FLOAT)) as rapport_score,
                AVG(CAST(accuracy->'scores'->'creatingInterest'->>'score' AS FLOAT)) as interest_score,
                AVG(CAST(accuracy->'scores'->'probing'->>'score' AS FLOAT)) as probing_score,
                AVG(CAST(accuracy->'scores'->'productKnowledge'->>'score' AS FLOAT)) as product_score,
                COUNT(*) as total_simulations,
                AVG(CASE 
                    WHEN conversation_data->'analysis'->'evaluation_criteria_results'->'introduction'->>'result' = 'success' THEN 100
                    ELSE 0
                END) as improvement_rate
            FROM call_sim_scoring
            WHERE accuracy IS NOT NULL
            AND team_id::text != %s
            GROUP BY team_id
        ),
        overall_benchmark AS (
            SELECT 
                AVG((intro_score + rapport_score + interest_score + probing_score + product_score) / 5) as overall_benchmark_score,
                AVG(total_simulations) as simulations_benchmark,
                AVG(improvement_rate) as improvement_benchmark
            FROM all_scores
            WHERE intro_score IS NOT NULL 
            AND rapport_score IS NOT NULL 
            AND interest_score IS NOT NULL 
            AND probing_score IS NOT NULL 
            AND product_score IS NOT NULL
        ),
        team_scores AS (
            SELECT 
                team_id,
                AVG(CAST(accuracy->'scores'->'introduction'->>'score' AS FLOAT)) as intro_score,
                AVG(CAST(accuracy->'scores'->'rapport'->>'score' AS FLOAT)) as rapport_score,
                AVG(CAST(accuracy->'scores'->'creatingInterest'->>'score' AS FLOAT)) as interest_score,
                AVG(CAST(accuracy->'scores'->'probing'->>'score' AS FLOAT)) as probing_score,
                AVG(CAST(accuracy->'scores'->'productKnowledge'->>'score' AS FLOAT)) as product_score,
                COUNT(*) as total_simulations,
                AVG(CASE 
                    WHEN conversation_data->'analysis'->'evaluation_criteria_results'->'introduction'->>'result' = 'success' THEN 100
                    ELSE 0
                END) as improvement_rate
            FROM call_sim_scoring
            WHERE team_id::text = %s
            {product_filter}
            GROUP BY team_id
        ),
        benchmark_results AS (
            SELECT 
                'Overall Score' as metric,
                AVG((intro_score + rapport_score + interest_score + probing_score + product_score) / 5) as team_average,
                (SELECT overall_benchmark_score FROM overall_benchmark) as industry_benchmark,
                ROUND((AVG((intro_score + rapport_score + interest_score + probing_score + product_score) / 5) - (SELECT overall_benchmark_score FROM overall_benchmark))::numeric, 1) as difference,
                1 as sort_order
            FROM team_scores
            WHERE intro_score IS NOT NULL 
            AND rapport_score IS NOT NULL 
            AND interest_score IS NOT NULL 
            AND probing_score IS NOT NULL 
            AND product_score IS NOT NULL
            UNION ALL
            SELECT 
                'Introduction' as metric,
                AVG(intro_score) as team_average,
                (SELECT AVG(intro_score) FROM all_scores) as industry_benchmark,
                ROUND((AVG(intro_score) - (SELECT AVG(intro_score) FROM all_scores))::numeric, 1) as difference,
                2 as sort_order
            FROM team_scores
            WHERE intro_score IS NOT NULL
            UNION ALL
            SELECT 
                'Rapport' as metric,
                AVG(rapport_score) as team_average,
                (SELECT AVG(rapport_score) FROM all_scores) as industry_benchmark,
                ROUND((AVG(rapport_score) - (SELECT AVG(rapport_score) FROM all_scores))::numeric, 1) as difference,
                3 as sort_order
            FROM team_scores
            WHERE rapport_score IS NOT NULL
            UNION ALL
            SELECT 
                'Interest' as metric,
                AVG(interest_score) as team_average,
                (SELECT AVG(interest_score) FROM all_scores) as industry_benchmark,
                ROUND((AVG(interest_score) - (SELECT AVG(interest_score) FROM all_scores))::numeric, 1) as difference,
                4 as sort_order
            FROM team_scores
            WHERE interest_score IS NOT NULL
            UNION ALL
            SELECT 
                'Probing' as metric,
                AVG(probing_score) as team_average,
                (SELECT AVG(probing_score) FROM all_scores) as industry_benchmark,
                ROUND((AVG(probing_score) - (SELECT AVG(probing_score) FROM all_scores))::numeric, 1) as difference,
                5 as sort_order
            FROM team_scores
            WHERE probing_score IS NOT NULL
            UNION ALL
            SELECT 
                'Product' as metric,
                AVG(product_score) as team_average,
                (SELECT AVG(product_score) FROM all_scores) as industry_benchmark,
                ROUND((AVG(product_score) - (SELECT AVG(product_score) FROM all_scores))::numeric, 1) as difference,
                6 as sort_order
            FROM team_scores
            WHERE product_score IS NOT NULL
            UNION ALL
            SELECT 
                'Simulations Completed' as metric,
                AVG(total_simulations) as team_average,
                (SELECT simulations_benchmark FROM overall_benchmark) as industry_benchmark,
                ROUND(((AVG(total_simulations) - (SELECT simulations_benchmark FROM overall_benchmark)) / NULLIF((SELECT simulations_benchmark FROM overall_benchmark), 0) * 100)::numeric, 1) as difference,
                7 as sort_order
            FROM team_scores
            WHERE total_simulations IS NOT NULL
        )
        SELECT 
            metric,
            team_average,
            industry_benchmark,
            difference
        FROM benchmark_results
        ORDER BY sort_order
    """
    
    # Add product filter if specified
    product_filter = ""
    params = [team_id, team_id]  # team_id is used twice - once for excluding from benchmark, once for team scores
    if product_id and product_id != 'all':
        product_filter = "AND product_id = %s"
        params.append(product_id)
    
    query = query.format(product_filter=product_filter)

    # Execute query
    cursor.execute(query, params)
    results = cursor.fetchall()

    if not results:
        return []

    # Format results for frontend
    benchmark_data = [
        {
            "metric": row[0],
            "teamAverage": float(round(row[1] or 0, 1)),
            "industryBenchmark": float(round(row[2] or 0, 1)),
            "difference": f"{'+' if row[3] >= 0 else ''}{float(round(row[3] or 0, 1))}%"
        }
        for row in results
    ]

    return benchmark_data

def calculate_adoption_data(cursor, product_id=None, team_id=None):
    """
    Calculate adoption level comparison data from call_sim_scoring table
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
            AND team_id::text != %s
        ),
        benchmarks AS (
            SELECT 
                adoption_continuum,
                AVG((intro_score + rapport_score + interest_score + probing_score + product_score) / 5) as benchmark_score
            FROM all_scores
            WHERE intro_score IS NOT NULL 
            AND rapport_score IS NOT NULL 
            AND interest_score IS NOT NULL 
            AND probing_score IS NOT NULL 
            AND product_score IS NOT NULL
            GROUP BY adoption_continuum
        ),
        overall_benchmark AS (
            SELECT AVG((intro_score + rapport_score + interest_score + probing_score + product_score) / 5) as overall_benchmark_score
            FROM all_scores
            WHERE intro_score IS NOT NULL 
            AND rapport_score IS NOT NULL 
            AND interest_score IS NOT NULL 
            AND probing_score IS NOT NULL 
            AND product_score IS NOT NULL
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
        ),
        adoption_results AS (
            SELECT 
                INITCAP(t.adoption_continuum) as type,
                AVG((t.intro_score + t.rapport_score + t.interest_score + t.probing_score + t.product_score) / 5) as team_average,
                b.benchmark_score as industry_benchmark,
                ROUND((AVG((t.intro_score + t.rapport_score + t.interest_score + t.probing_score + t.product_score) / 5) - b.benchmark_score)::numeric, 1) as difference,
                0 as sort_order
            FROM team_scores t
            JOIN benchmarks b ON t.adoption_continuum = b.adoption_continuum
            WHERE t.intro_score IS NOT NULL 
            AND t.rapport_score IS NOT NULL 
            AND t.interest_score IS NOT NULL 
            AND t.probing_score IS NOT NULL 
            AND t.product_score IS NOT NULL
            GROUP BY t.adoption_continuum, b.benchmark_score
            UNION ALL
            SELECT 
                'Overall' as type,
                AVG((t.intro_score + t.rapport_score + t.interest_score + t.probing_score + t.product_score) / 5) as team_average,
                (SELECT overall_benchmark_score FROM overall_benchmark) as industry_benchmark,
                ROUND((AVG((t.intro_score + t.rapport_score + t.interest_score + t.probing_score + t.product_score) / 5) - (SELECT overall_benchmark_score FROM overall_benchmark))::numeric, 1) as difference,
                1 as sort_order
            FROM team_scores t
            WHERE t.intro_score IS NOT NULL 
            AND t.rapport_score IS NOT NULL 
            AND t.interest_score IS NOT NULL 
            AND t.probing_score IS NOT NULL 
            AND t.product_score IS NOT NULL
        )
        SELECT 
            type,
            team_average,
            industry_benchmark,
            difference
        FROM adoption_results
        ORDER BY sort_order, type
    """
    
    # Add product filter if specified
    product_filter = ""
    params = [team_id, team_id]  # team_id is used twice - once for excluding from benchmark, once for team scores
    if product_id and product_id != 'all':
        product_filter = "AND product_id = %s"
        params.append(product_id)
    
    query = query.format(product_filter=product_filter)

    # Execute query
    cursor.execute(query, params)
    results = cursor.fetchall()

    if not results:
        return []

    # Format results for frontend
    adoption_data = [
        {
            "type": row[0],
            "teamAverage": float(round(row[1] or 0, 1)),
            "industryBenchmark": float(round(row[2] or 0, 1)),
            "difference": f"{'+' if row[3] >= 0 else ''}{float(round(row[3] or 0, 1))}%"
        }
        for row in results
    ]

    return adoption_data

def calculate_situation_data(cursor, product_id=None, team_id=None):
    """
    Calculate situation comparison data from call_sim_scoring table
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
            AND team_id::text != %s
        ),
        benchmarks AS (
            SELECT 
                situation,
                AVG((intro_score + rapport_score + interest_score + probing_score + product_score) / 5) as benchmark_score
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
        ),
        overall_benchmark AS (
            SELECT AVG((intro_score + rapport_score + interest_score + probing_score + product_score) / 5) as overall_benchmark_score
            FROM all_scores
            WHERE intro_score IS NOT NULL 
            AND rapport_score IS NOT NULL 
            AND interest_score IS NOT NULL 
            AND probing_score IS NOT NULL 
            AND product_score IS NOT NULL
        ),
        situation_results AS (
            SELECT 
                INITCAP(t.situation) as situation,
                AVG((t.intro_score + t.rapport_score + t.interest_score + t.probing_score + t.product_score) / 5) as team_average,
                b.benchmark_score as industry_benchmark,
                ROUND((AVG((t.intro_score + t.rapport_score + t.interest_score + t.probing_score + t.product_score) / 5) - b.benchmark_score)::numeric, 1) as difference,
                0 as sort_order
            FROM team_scores t
            JOIN benchmarks b ON t.situation = b.situation
            WHERE t.intro_score IS NOT NULL 
            AND t.rapport_score IS NOT NULL 
            AND t.interest_score IS NOT NULL 
            AND t.probing_score IS NOT NULL 
            AND t.product_score IS NOT NULL
            GROUP BY t.situation, b.benchmark_score
            UNION ALL
            SELECT 
                'Overall' as situation,
                AVG((t.intro_score + t.rapport_score + t.interest_score + t.probing_score + t.product_score) / 5) as team_average,
                (SELECT overall_benchmark_score FROM overall_benchmark) as industry_benchmark,
                ROUND((AVG((t.intro_score + t.rapport_score + t.interest_score + t.probing_score + t.product_score) / 5) - (SELECT overall_benchmark_score FROM overall_benchmark))::numeric, 1) as difference,
                1 as sort_order
            FROM team_scores t
            WHERE t.intro_score IS NOT NULL 
            AND t.rapport_score IS NOT NULL 
            AND t.interest_score IS NOT NULL 
            AND t.probing_score IS NOT NULL 
            AND t.product_score IS NOT NULL
        )
        SELECT 
            situation,
            team_average,
            industry_benchmark,
            difference
        FROM situation_results
        ORDER BY sort_order, situation
    """
    
    # Add product filter if specified
    product_filter = ""
    params = [team_id, team_id]  # team_id is used twice - once for excluding from benchmark, once for team scores
    if product_id and product_id != 'all':
        product_filter = "AND product_id = %s"
        params.append(product_id)
    
    query = query.format(product_filter=product_filter)

    # Execute query
    cursor.execute(query, params)
    results = cursor.fetchall()

    if not results:
        return []

    # Format results for frontend
    situation_data = [
        {
            "situation": row[0],
            "teamAverage": float(round(row[1] or 0, 1)),
            "industryBenchmark": float(round(row[2] or 0, 1)),
            "difference": f"{'+' if row[3] >= 0 else ''}{float(round(row[3] or 0, 1))}%"
        }
        for row in results
    ]

    return situation_data

def get_filter_options(cursor, team_id=None):
    """
    Get available teams and products for filters
    """
    # Get available teams
    teams_query = """
        SELECT DISTINCT team_id 
        FROM call_sim_scoring 
        WHERE team_id IS NOT NULL
    """
    cursor.execute(teams_query)
    teams = [row[0] for row in cursor.fetchall()]

    # Get available products for the specific team
    products_query = """
        SELECT DISTINCT product_id 
        FROM call_sim_scoring 
        WHERE product_id IS NOT NULL
        AND team_id = %s
    """
    cursor.execute(products_query, [team_id])
    products = [row[0] for row in cursor.fetchall()]

    return {
        "teams": teams,
        "products": products
    }

def handle_benchmarks_request(event, context):
    # Get query parameters and path
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
        
        # Get filters from query parameters
        product_id = query_params.get('product')
        team_id = query_params.get('team')
        
        # Handle different endpoints
        if path == 'industry-benchmarks':
            # Get filter options with team_id to filter products
            filter_options = get_filter_options(cursor, team_id)
            
            # Get skill data
            skill_data = calculate_skill_data(cursor, product_id, team_id)
            
            if not skill_data:
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
                "body": json.dumps({
                    "skillData": skill_data,
                    "filterOptions": filter_options
                })
            }
        elif path == 'industry-benchmarks/detail':
            # Get benchmark data
            benchmark_data = calculate_benchmark_data(cursor, product_id, team_id)
            
            if not benchmark_data:
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
                "body": json.dumps({
                    "benchmarkData": benchmark_data
                })
            }
        elif path == 'industry-benchmarks/adoption':
            # Get adoption data
            adoption_data = calculate_adoption_data(cursor, product_id, team_id)
            
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
                "body": json.dumps({
                    "adoptionData": adoption_data
                })
            }
        elif path == 'industry-benchmarks/situation':
            try:
                # Get situation data
                situation_data = calculate_situation_data(cursor, product_id, team_id)
                
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
                
                # Get filter options
                filter_options = get_filter_options(cursor, team_id)
                
                return {
                    "statusCode": 200,
                    "headers": {
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Headers": "*",
                        "Access-Control-Allow-Methods": "*"
                    },
                    "body": json.dumps({
                        "situationData": situation_data,
                        "filterOptions": filter_options
                    })
                }
            except Exception as e:
                print(f"Error in situation endpoint: {str(e)}")
                raise
        
        # Return 404 for unknown paths
        return {
            "statusCode": 404,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "message": "Endpoint not found",
                "path": path
            })
        }
            
    except Exception as e:
        print(f"Database error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "error": f"Database error occurred: {str(e)}"
            })
        }
    finally:
        if 'connection' in locals() and connection:
            cursor.close()
            connection.close() 