import json

def handle_recommendations_request(event, context):
    # Get query parameters and path
    query_params = event.get('queryStringParameters', {}) or {}
    path = event.get('path', '')
    
    # Remove leading slash if present
    path = path.lstrip('/')
    
    # Debug logging
    print(f"Recommendations handler received path: {path}")
    
    # Base recommendations data
    recommendations_data = {
        "teamStrengths": [
            {
                "id": 1,
                "title": "Strong Introduction Skills",
                "description": "Team demonstrates excellent opening and rapport building skills"
            },
            {
                "id": 2,
                "title": "Effective Communication",
                "description": "Clear and concise delivery with natural conversation flow"
            }
        ],
        "areasForImprovement": [
            {
                "id": 1,
                "title": "Product Knowledge Enhancement",
                "description": "Opportunity to deepen understanding of product features and benefits"
            },
            {
                "id": 2,
                "title": "Customer Engagement",
                "description": "Build stronger connections through active listening and open-ended questions"
            }
        ],
        "trainingFocus": [
            {
                "id": 1,
                "title": "Advanced Product Knowledge",
                "description": "Deep dive into product features and benefits through interactive workshops"
            },
            {
                "id": 2,
                "title": "Rapport Building Techniques",
                "description": "Learn effective customer engagement strategies through role-playing scenarios"
            }
        ],
        "developmentPlans": [
            {
                "teamMember": "John Doe",
                "primaryFocus": "Product Expertise",
                "secondaryFocus": "Customer Engagement",
                "recommendedTraining": "Advanced Product Workshop"
            },
            {
                "teamMember": "Jane Smith",
                "primaryFocus": "Customer Engagement",
                "secondaryFocus": "Product Knowledge",
                "recommendedTraining": "Rapport Building Course"
            }
        ],
        "simulationStrategies": [
            "Implement structured product training modules",
            "Conduct weekly role-playing sessions",
            "Review and analyze customer feedback",
            "Practice product demonstrations",
            "Participate in peer mentoring sessions"
        ]
    }

    # Handle different endpoints
    if path == 'insights-recommendations':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps(recommendations_data)
        }
    elif path == 'insights-recommendations/strengths':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "teamStrengths": recommendations_data["teamStrengths"]
            })
        }
    elif path == 'insights-recommendations/improvements':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "areasForImprovement": recommendations_data["areasForImprovement"]
            })
        }
    elif path == 'insights-recommendations/training':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "trainingFocus": recommendations_data["trainingFocus"]
            })
        }
    elif path == 'insights-recommendations/development':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "developmentPlans": recommendations_data["developmentPlans"]
            })
        }
    elif path == 'insights-recommendations/strategies':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "simulationStrategies": recommendations_data["simulationStrategies"]
            })
        }
    
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