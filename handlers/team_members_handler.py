import json

def handle_team_members_request(event, context):
    path = event.get('path', '')
    
    # Remove leading slash if present
    path = path.lstrip('/')
    
    # Debug logging
    print(f"Team members handler received path: {path}")
    
    # Base team members data
    team_members_data = {
        "teamMembers": [
            {
                "id": 1,
                "name": "John Smith",
                "team": "North Region",
                "region": "Northeast",
                "overallScore": 78,
                "simulations": 12,
                "improvement": 15,
                "adoptionLevel": "Adopter",
                "topSkill": "Introduction",
                "needsImprovement": "Product Knowledge",
                "skillBreakdown": {
                    "Fluency": 80,
                    "Introduction": 85,
                    "Rapport": 75,
                    "Interest": 82,
                    "Probing": 78,
                    "Product": 72
                },
                "trendData": [
                    {
                        "month": "Jan",
                        "score": 65
                    },
                    {
                        "month": "Feb",
                        "score": 68
                    },
                    {
                        "month": "Mar",
                        "score": 72
                    },
                    {
                        "month": "Apr",
                        "score": 78
                    }
                ],
                "situationData": [
                    {
                        "name": "Appointment",
                        "count": 8,
                        "average": 80
                    },
                    {
                        "name": "Counter Call",
                        "count": 3,
                        "average": 75
                    },
                    {
                        "name": "Lunch & Learn",
                        "count": 1,
                        "average": 85
                    }
                ]
            },
            {
                "id": 2,
                "name": "Sarah Johnson",
                "team": "South Region",
                "region": "Southeast",
                "overallScore": 82,
                "simulations": 15,
                "improvement": 20,
                "adoptionLevel": "Advocate",
                "topSkill": "Fluency",
                "needsImprovement": "Rapport",
                "skillBreakdown": {
                    "Fluency": 85,
                    "Introduction": 88,
                    "Rapport": 80,
                    "Interest": 85,
                    "Probing": 82,
                    "Product": 78
                },
                "trendData": [
                    {
                        "month": "Jan",
                        "score": 68
                    },
                    {
                        "month": "Feb",
                        "score": 72
                    },
                    {
                        "month": "Mar",
                        "score": 78
                    },
                    {
                        "month": "Apr",
                        "score": 82
                    }
                ],
                "situationData": [
                    {
                        "name": "Appointment",
                        "count": 10,
                        "average": 85
                    },
                    {
                        "name": "Counter Call",
                        "count": 4,
                        "average": 80
                    },
                    {
                        "name": "Lunch & Learn",
                        "count": 1,
                        "average": 90
                    }
                ]
            }
        ],
        "filterOptions": {
            "teams": ["North Region", "South Region", "East Region", "West Region"],
            "skills": ["Overall", "Fluency", "Introduction", "Rapport", "Interest", "Probing", "Product"]
        }
    }

    # Handle member details endpoint
    if path.startswith('team-members/'):
        member_id = int(path.split('/')[-1])
        member = next((m for m in team_members_data["teamMembers"] if m["id"] == member_id), None)
        
        if member:
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*"
                },
                "body": json.dumps(member)
            }
        else:
            return {
                "statusCode": 404,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*"
                },
                "body": json.dumps({
                    "message": "Member not found",
                    "path": path
                })
            }
    
    # Return all team members for the main endpoint
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*"
        },
        "body": json.dumps(team_members_data)
    } 
