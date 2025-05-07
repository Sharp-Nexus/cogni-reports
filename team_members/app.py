import json

def get_team_members(filters=None):
    team_members = [
        {
            "id": "tm1",
            "name": "Alex Johnson",
            "region": "East Region",
            "team": "Team A",
            "overallScore": 72,
            "vsBenchmark": 2,
            "simulations": 12,
            "topSkill": "Introduction",
            "needsImprovement": "Product Knowledge",
            "bestScenario": "Appointment",
            "skillBreakdown": {
                "Fluency": 75,
                "Introduction": 82,
                "Rapport": 70,
                "Interest": 68,
                "Probing": 72,
                "Product": 65
            }
        },
        {
            "id": "tm2",
            "name": "Morgan Smith",
            "region": "West Region",
            "team": "Team B",
            "overallScore": 85,
            "vsBenchmark": 15,
            "simulations": 15,
            "topSkill": "Introduction",
            "needsImprovement": "Rapport",
            "bestScenario": "Appointment",
            "skillBreakdown": {
                "Fluency": 88,
                "Introduction": 90,
                "Rapport": 78,
                "Interest": 85,
                "Probing": 84,
                "Product": 82
            }
        },
        {
            "id": "tm3",
            "name": "Taylor Wilson",
            "region": "North Region",
            "team": "Team A",
            "overallScore": 68,
            "vsBenchmark": -2,
            "simulations": 10,
            "topSkill": "Introduction",
            "needsImprovement": "Rapport",
            "bestScenario": "Appointment",
            "skillBreakdown": {
                "Fluency": 70,
                "Introduction": 78,
                "Rapport": 60,
                "Interest": 65,
                "Probing": 67,
                "Product": 66
            }
        },
        {
            "id": "tm4",
            "name": "Jordan Lee",
            "region": "South Region",
            "team": "Team C",
            "overallScore": 78,
            "vsBenchmark": 8,
            "simulations": 14,
            "topSkill": "Introduction",
            "needsImprovement": "Rapport",
            "bestScenario": "Appointment",
            "skillBreakdown": {
                "Fluency": 80,
                "Introduction": 83,
                "Rapport": 74,
                "Interest": 77,
                "Probing": 75,
                "Product": 79
            }
        },
        {
            "id": "tm5",
            "name": "Casey Brown",
            "region": "Central Region",
            "team": "Team B",
            "overallScore": 62,
            "vsBenchmark": -8,
            "simulations": 8,
            "topSkill": "Introduction",
            "needsImprovement": "Rapport",
            "bestScenario": "Appointment",
            "skillBreakdown": {
                "Fluency": 66,
                "Introduction": 69,
                "Rapport": 58,
                "Interest": 60,
                "Probing": 63,
                "Product": 56
            }
        }
    ]
    
    # Get unique team names for filter options
    teams = sorted(list(set(member["team"] for member in team_members)))
    
    # If no filters provided, just return the team options (for initial load)
    if not filters:
        return {
            "teamMembers": [],
            "filterOptions": {
                "teams": teams,
                "skills": ["Overall", "Fluency", "Introduction", "Rapport", "Interest", "Probing", "Product"]
            }
        }
    
    # Default to first team if no team specified
    if 'team' not in filters or not filters['team']:
        if teams:
            filters['team'] = teams[0]
    
    # Apply team filter - this is now required
    filtered_members = [member for member in team_members if member["team"] == filters['team']]
    
    # Calculate dynamic benchmarks for each skill
    benchmarks = {}
    if filtered_members:
        # Overall benchmark
        benchmarks["Overall"] = sum(member["overallScore"] for member in filtered_members) / len(filtered_members)
        
        # Skill-specific benchmarks
        skills = ["Fluency", "Introduction", "Rapport", "Interest", "Probing", "Product"]
        for skill in skills:
            skill_scores = [member["skillBreakdown"][skill] for member in filtered_members]
            benchmarks[skill] = sum(skill_scores) / len(skill_scores)
    
    # Update vsBenchmark values based on dynamic benchmarks
    for member in filtered_members:
        # Update overall benchmark comparison
        member["vsBenchmark"] = round(member["overallScore"] - benchmarks["Overall"])
        
        # We could also add skill-specific benchmark comparisons here if needed
    
    if 'skill' in filters and filters['skill'] and filters['skill'] != 'Overall':
        # Sort by specific skill if requested
        filtered_members.sort(key=lambda x: x["skillBreakdown"][filters['skill']], reverse=True)
    else:
        # Default sort by overall score
        filtered_members.sort(key=lambda x: x["overallScore"], reverse=True)
    
    # Get skills list
    skills = ["Overall", "Fluency", "Introduction", "Rapport", "Interest", "Probing", "Product"]
    
    return {
        "teamMembers": filtered_members,
        "filterOptions": {
            "teams": teams,
            "skills": skills
        }
    }

def get_team_member_details(member_id):
    # Get all team members without filtering by team
    all_team_members = [
        {
            "id": "tm1",
            "name": "Alex Johnson",
            "region": "East Region",
            "team": "Team A",
            "overallScore": 72,
            "vsBenchmark": 2,
            "simulations": 12,
            "topSkill": "Introduction",
            "needsImprovement": "Product Knowledge",
            "bestScenario": "Appointment",
            "skillBreakdown": {
                "Fluency": 75,
                "Introduction": 82,
                "Rapport": 70,
                "Interest": 68,
                "Probing": 72,
                "Product": 65
            }
        },
        {
            "id": "tm2",
            "name": "Morgan Smith",
            "region": "West Region",
            "team": "Team B",
            "overallScore": 85,
            "vsBenchmark": 15,
            "simulations": 15,
            "topSkill": "Introduction",
            "needsImprovement": "Rapport",
            "bestScenario": "Appointment",
            "skillBreakdown": {
                "Fluency": 88,
                "Introduction": 90,
                "Rapport": 78,
                "Interest": 85,
                "Probing": 84,
                "Product": 82
            }
        },
        {
            "id": "tm3",
            "name": "Taylor Wilson",
            "region": "North Region",
            "team": "Team A",
            "overallScore": 68,
            "vsBenchmark": -2,
            "simulations": 10,
            "topSkill": "Introduction",
            "needsImprovement": "Rapport",
            "bestScenario": "Appointment",
            "skillBreakdown": {
                "Fluency": 70,
                "Introduction": 78,
                "Rapport": 60,
                "Interest": 65,
                "Probing": 67,
                "Product": 66
            }
        },
        {
            "id": "tm4",
            "name": "Jordan Lee",
            "region": "South Region",
            "team": "Team C",
            "overallScore": 78,
            "vsBenchmark": 8,
            "simulations": 14,
            "topSkill": "Introduction",
            "needsImprovement": "Rapport",
            "bestScenario": "Appointment",
            "skillBreakdown": {
                "Fluency": 80,
                "Introduction": 83,
                "Rapport": 74,
                "Interest": 77,
                "Probing": 75,
                "Product": 79
            }
        },
        {
            "id": "tm5",
            "name": "Casey Brown",
            "region": "Central Region",
            "team": "Team B",
            "overallScore": 62,
            "vsBenchmark": -8,
            "simulations": 8,
            "topSkill": "Introduction",
            "needsImprovement": "Rapport",
            "bestScenario": "Appointment",
            "skillBreakdown": {
                "Fluency": 66,
                "Introduction": 69,
                "Rapport": 58,
                "Interest": 60,
                "Probing": 63,
                "Product": 56
            }
        }
    ]
    
    member = next((m for m in all_team_members if m["id"] == member_id), None)
    
    if not member:
        return None
    
    # Get team-specific benchmark for this member's team
    team_members = [m for m in all_team_members if m["team"] == member["team"]]
    team_benchmark = sum(m["overallScore"] for m in team_members) / len(team_members)
    
    # Update vsBenchmark value
    member["vsBenchmark"] = round(member["overallScore"] - team_benchmark)
    
    return {
        "member": member,
        "performanceHistory": [
            {"week": "Week 1", "score": 65},
            {"week": "Week 2", "score": 68},
            {"week": "Week 3", "score": 70},
            {"week": "Week 4", "score": member["overallScore"]}
        ],
        "skillBreakdown": [
            {"skill": "Fluency", "score": member["skillBreakdown"]["Fluency"]},
            {"skill": "Introduction", "score": member["skillBreakdown"]["Introduction"]},
            {"skill": "Rapport", "score": member["skillBreakdown"]["Rapport"]},
            {"skill": "Interest", "score": member["skillBreakdown"]["Interest"]},
            {"skill": "Probing", "score": member["skillBreakdown"]["Probing"]},
            {"skill": "Product", "score": member["skillBreakdown"]["Product"]}
        ]
    }

# Route dictionary mapping paths to their respective handler functions
ROUTES = {
    '/team-members': get_team_members
}

def lambda_handler(event, context):
    # Get the path from the event
    path = event.get('path', '')
    
    # Get query parameters for filtering
    query_params = event.get('queryStringParameters', {}) or {}
    filters = {}
    
    if 'team' in query_params:
        filters['team'] = query_params['team']
    
    if 'skill' in query_params:
        filters['skill'] = query_params['skill']
    
    # Check if it's a team member details request
    if path.startswith('/team-members/') and len(path.split('/')) > 2:
        member_id = path.split('/')[-1]
        data = get_team_member_details(member_id)
        if not data:
            return {
                "statusCode": 404,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "*"
                },
                "body": json.dumps({"error": "Team member not found"})
            }
    else:
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
        data = handler(filters)

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