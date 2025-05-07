import json

def get_team_strengths():
    return {
        "teamStrengths": [
            {
                "id": 1,
                "title": "Introduction Skills",
                "description": "The team excels at introducing themselves and the product effectively, scoring consistently higher than the industry benchmark."
            },
            {
                "id": 2,
                "title": "Creating Interest",
                "description": "Team members are effective at generating customer curiosity and interest, with an average score well above the industry benchmark."
            },
            {
                "id": 3,
                "title": "Appointment Scenarios",
                "description": "The team performs particularly well in formal appointment settings, scoring higher than the industry average in these situations."
            }
        ]
    }

def get_areas_for_improvement():
    return {
        "areasForImprovement": [
            {
                "id": 1,
                "title": "Rapport Building",
                "description": "The team struggles with establishing personal connections, scoring below the industry benchmark in this critical area."
            },
            {
                "id": 2,
                "title": "Counter Call Interactions",
                "description": "Brief interactions are challenging for the team, with a score below the industry average in these high-pressure situations."
            },
            {
                "id": 3,
                "title": "Naive Customer Approach",
                "description": "The team needs to improve their approach with less knowledgeable customers, scoring below the benchmark when dealing with this customer segment."
            }
        ]
    }

def get_training_focus():
    return {
        "trainingFocus": [
            {
                "id": 1,
                "title": "Rapport Building Workshop",
                "description": "Schedule a dedicated workshop focused on rapport-building techniques. Include role-playing exercises with different customer personas and provide specific scripts and questions that can help establish personal connections quickly."
            },
            {
                "id": 2,
                "title": "Counter Call Efficiency Training",
                "description": "Develop a specialized training module for brief interactions. Focus on creating concise value propositions that can be delivered in under 30 seconds and practice quick needs assessment techniques."
            },
            {
                "id": 3,
                "title": "Customer Knowledge Adaptation",
                "description": "Create simulation scenarios specifically targeting naive customers. Train the team to quickly assess customer knowledge levels and adjust their approach accordingly, focusing on educational content for less knowledgeable customers."
            }
        ]
    }

def get_development_plans():
    return {
        "developmentPlans": [
            {
                "teamMember": "Alex Johnson",
                "primaryFocus": "Rapport Building",
                "secondaryFocus": "Counter Call Efficiency",
                "recommendedTraining": "1-on-1 Coaching, Role Play Exercises"
            },
            {
                "teamMember": "Morgan Smith",
                "primaryFocus": "Naive Customer Approach",
                "secondaryFocus": "Product Knowledge",
                "recommendedTraining": "Advanced Product Training, Simplification Techniques"
            },
            {
                "teamMember": "Taylor Wilson",
                "primaryFocus": "Rapport Building",
                "secondaryFocus": "Probing Skills",
                "recommendedTraining": "Question Technique Workshop, Active Listening Training"
            },
            {
                "teamMember": "Jordan Lee",
                "primaryFocus": "Counter Call Efficiency",
                "secondaryFocus": "Rapport Building",
                "recommendedTraining": "Brief Interaction Simulations, Connection Building Workshop"
            },
            {
                "teamMember": "Casey Brown",
                "primaryFocus": "Overall Performance",
                "secondaryFocus": "Product Knowledge",
                "recommendedTraining": "Comprehensive Refresher Course, Shadowing Top Performers"
            }
        ]
    }

def get_simulation_strategies():
    return {
        "simulationStrategies": [
            "Increase the frequency of Counter Call simulations to address the team's weakest scenario",
            "Create more scenarios featuring Naive customers to improve performance with this adoption level",
            "Implement peer review sessions where team members can observe and provide feedback on each other's simulations",
            "Develop progressive difficulty levels that gradually increase complexity as team members improve",
            "Set specific improvement targets for each team member based on their individual performance data"
        ]
    }

def get_all_recommendations():
    return {
        "teamStrengths": get_team_strengths()["teamStrengths"],
        "areasForImprovement": get_areas_for_improvement()["areasForImprovement"],
        "trainingFocus": get_training_focus()["trainingFocus"],
        "developmentPlans": get_development_plans()["developmentPlans"],
        "simulationStrategies": get_simulation_strategies()["simulationStrategies"]
    }

# Route dictionary mapping paths to their respective handler functions
ROUTES = {
    '/insights-recommendations': get_all_recommendations,
    '/insights-recommendations/strengths': get_team_strengths,
    '/insights-recommendations/improvements': get_areas_for_improvement,
    '/insights-recommendations/training': get_training_focus,
    '/insights-recommendations/development': get_development_plans,
    '/insights-recommendations/strategies': get_simulation_strategies
}

def lambda_handler(event, context):
    # Get the path from the event
    path = event.get('path', '')
    
    # Get the handler function from the routes dictionary
    handler = ROUTES.get(path)
    
    if handler is None:
        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({"error": "Endpoint not found"})
        }
    
    # Execute the handler function to get the data
    data = handler()

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*"
        },
        "body": json.dumps(data)
    } 