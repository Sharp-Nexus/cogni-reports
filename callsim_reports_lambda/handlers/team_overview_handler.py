import json

def handle_team_overview_request(event, context):
    # Get query parameters
    query_params = event.get('queryStringParameters', {}) or {}
    path = event.get('path', '')
    
    # Remove leading slash if present
    path = path.lstrip('/')
    
    # Debug logging
    print(f"Team overview handler received path: {path}")
    
    # Base team overview data
    team_overview_data = {
        "teamAverages": {
            "overall": 75,
            "simulations": 82,
            "improvement": 15
        },
        "industryBenchmarks": {
            "overall": 68
        },
        "teamComparisonData": [
            {
                "name": "Overall Score",
                "team": 75,
                "average": 68
            },
            {
                "name": "Fluency",
                "team": 78,
                "average": 72
            },
            {
                "name": "Introduction",
                "team": 82,
                "average": 75
            },
            {
                "name": "Rapport",
                "team": 70,
                "average": 65
            },
            {
                "name": "Interest",
                "team": 80,
                "average": 73
            },
            {
                "name": "Probing",
                "team": 75,
                "average": 70
            },
            {
                "name": "Product Knowledge",
                "team": 72,
                "average": 68
            }
        ],
        "teamTrendData": [
            {
                "name": "Jan",
                "team": 65,
                "industry": 62
            },
            {
                "name": "Feb",
                "team": 68,
                "industry": 63
            },
            {
                "name": "Mar",
                "team": 72,
                "industry": 65
            },
            {
                "name": "Apr",
                "team": 75,
                "industry": 68
            }
        ],
        "adoptionData": [
            {
                "name": "Passive",
                "team": 20,
                "industry": 25
            },
            {
                "name": "Evaluator",
                "team": 35,
                "industry": 40
            },
            {
                "name": "Adopter",
                "team": 30,
                "industry": 25
            },
            {
                "name": "Advocate",
                "team": 15,
                "industry": 10
            }
        ],
        "situationData": [
            {
                "name": "Appointment",
                "team": 45,
                "industry": 40
            },
            {
                "name": "Counter Call",
                "team": 25,
                "industry": 30
            },
            {
                "name": "Lunch & Learn",
                "team": 20,
                "industry": 20
            },
            {
                "name": "Other",
                "team": 10,
                "industry": 10
            }
        ]
    }

    # Handle different endpoints
    if path == 'team-overview':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps(team_overview_data)
        }
    elif path == 'team-overview/averages':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "teamAverages": team_overview_data["teamAverages"],
                "industryBenchmarks": team_overview_data["industryBenchmarks"]
            })
        }
    elif path == 'team-overview/comparison':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "teamComparisonData": team_overview_data["teamComparisonData"]
            })
        }
    elif path == 'team-overview/trend':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "teamTrendData": team_overview_data["teamTrendData"]
            })
        }
    elif path == 'team-overview/adoption':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "adoptionData": team_overview_data["adoptionData"]
            })
        }
    elif path == 'team-overview/situation':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "situationData": team_overview_data["situationData"]
            })
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