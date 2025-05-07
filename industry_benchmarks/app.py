import json

# Sample team data with product-specific metrics only
TEAM_DATA = {
    "Team A": {
        "products": {
            "Besophil": {
                "overallScore": 78,
                "skills": {
                    "Fluency": 80,
                    "Introduction": 84,
                    "Rapport": 72,
                    "Interest": 80,
                    "Probing": 76,
                    "Product": 74
                },
                "adoption": {
                    "Naive": 71,
                    "Passive": 75,
                    "Evaluator": 82,
                    "Adopter": 84,
                    "Advocate": 80
                },
                "situation": {
                    "Counter Call": 75,
                    "Appointment": 81,
                    "Lunch & Learn": 78
                }
            },
            "ELF": {
                "overallScore": 74,
                "skills": {
                    "Fluency": 76,
                    "Introduction": 80,
                    "Rapport": 68,
                    "Interest": 76,
                    "Probing": 72,
                    "Product": 70
                },
                "adoption": {
                    "Naive": 67,
                    "Passive": 71,
                    "Evaluator": 78,
                    "Adopter": 80,
                    "Advocate": 76
                },
                "situation": {
                    "Counter Call": 71,
                    "Appointment": 77,
                    "Lunch & Learn": 74
                }
            }
        }
    },
    "Team B": {
        "products": {
            "Besophil": {
                "overallScore": 72,
                "skills": {
                    "Fluency": 75,
                    "Introduction": 79,
                    "Rapport": 70,
                    "Interest": 74,
                    "Probing": 70,
                    "Product": 68
                },
                "adoption": {
                    "Naive": 66,
                    "Passive": 70,
                    "Evaluator": 75,
                    "Adopter": 77,
                    "Advocate": 73
                },
                "situation": {
                    "Counter Call": 70,
                    "Appointment": 76,
                    "Lunch & Learn": 72
                }
            },
            "ELF": {
                "overallScore": 68,
                "skills": {
                    "Fluency": 71,
                    "Introduction": 75,
                    "Rapport": 66,
                    "Interest": 70,
                    "Probing": 66,
                    "Product": 64
                },
                "adoption": {
                    "Naive": 62,
                    "Passive": 66,
                    "Evaluator": 71,
                    "Adopter": 73,
                    "Advocate": 69
                },
                "situation": {
                    "Counter Call": 66,
                    "Appointment": 72,
                    "Lunch & Learn": 68
                }
            }
        }
    },
    "Team C": {
        "products": {
            "Besophil": {
                "overallScore": 74,
                "skills": {
                    "Fluency": 77,
                    "Introduction": 81,
                    "Rapport": 69,
                    "Interest": 76,
                    "Probing": 72,
                    "Product": 71
                },
                "adoption": {
                    "Naive": 67,
                    "Passive": 72,
                    "Evaluator": 77,
                    "Adopter": 80,
                    "Advocate": 76
                },
                "situation": {
                    "Counter Call": 72,
                    "Appointment": 78,
                    "Lunch & Learn": 75
                }
            },
            "ELF": {
                "overallScore": 70,
                "skills": {
                    "Fluency": 73,
                    "Introduction": 77,
                    "Rapport": 65,
                    "Interest": 72,
                    "Probing": 68,
                    "Product": 67
                },
                "adoption": {
                    "Naive": 63,
                    "Passive": 68,
                    "Evaluator": 73,
                    "Adopter": 76,
                    "Advocate": 72
                },
                "situation": {
                    "Counter Call": 68,
                    "Appointment": 74,
                    "Lunch & Learn": 71
                }
            }
        }
    }
}

# Get available products from the data
def get_available_products():
    # Get products from the first team (assuming all teams have the same products)
    first_team = next(iter(TEAM_DATA.values()))
    return sorted(list(first_team.get("products", {}).keys()))

# Calculate dynamic industry benchmarks based on filter context
def calculate_industry_benchmarks(selected_team=None, selected_product=None):
    """Calculate industry benchmarks dynamically as the average of all other teams"""
    
    # Teams to include in the industry average (all teams except selected)
    teams_to_include = [team for team in TEAM_DATA.keys() if team != selected_team]
    
    if not teams_to_include:  # If no teams to include (should never happen)
        teams_to_include = list(TEAM_DATA.keys())
    
    # Initialize benchmark structure
    benchmarks = {
        "overall": 0,
        "skills": {
            "Fluency": 0,
            "Introduction": 0,
            "Rapport": 0,
            "Interest": 0,
            "Probing": 0,
            "Product": 0
        },
        "adoption": {
            "Naive": 0,
            "Passive": 0,
            "Evaluator": 0,
            "Adopter": 0,
            "Advocate": 0
        },
        "situation": {
            "Counter Call": 0,
            "Appointment": 0,
            "Lunch & Learn": 0
        }
    }
    
    # Calculate sums
    team_count = 0
    
    # If no product selected, we need a default
    if not selected_product:
        available_products = get_available_products()
        if available_products:
            selected_product = available_products[0]
        else:
            return benchmarks  # No products available
    
    for team_name in teams_to_include:
        team = TEAM_DATA[team_name]
        
        # Get product-specific data
        if selected_product and selected_product in team.get("products", {}):
            team_data = team["products"][selected_product]
            team_count += 1
            
            # Overall score
            benchmarks["overall"] += team_data["overallScore"]
            
            # Skills scores
            for skill in benchmarks["skills"].keys():
                benchmarks["skills"][skill] += team_data["skills"][skill]
            
            # Adoption scores
            for adoption in benchmarks["adoption"].keys():
                benchmarks["adoption"][adoption] += team_data["adoption"][adoption]
            
            # Situation scores
            for situation in benchmarks["situation"].keys():
                benchmarks["situation"][situation] += team_data["situation"][situation]
    
    # Calculate averages
    if team_count > 0:
        benchmarks["overall"] = round(benchmarks["overall"] / team_count)
        
        for skill in benchmarks["skills"].keys():
            benchmarks["skills"][skill] = round(benchmarks["skills"][skill] / team_count)
        
        for adoption in benchmarks["adoption"].keys():
            benchmarks["adoption"][adoption] = round(benchmarks["adoption"][adoption] / team_count)
        
        for situation in benchmarks["situation"].keys():
            benchmarks["situation"][situation] = round(benchmarks["situation"][situation] / team_count)
    
    return benchmarks

# Get team data based on filters
def get_team_data(team, product=None):
    """Get team data for the specified team and product"""
    if team not in TEAM_DATA:
        return None
    
    # Need to have a product - if none specified, use the first available
    if not product:
        products = list(TEAM_DATA[team].get("products", {}).keys())
        if not products:
            return None
        product = products[0]
        
    # Get product-specific data
    if product in TEAM_DATA[team].get("products", {}):
        return TEAM_DATA[team]["products"][product]
    
    return None

def get_skill_comparison(filters=None):
    # Get teams list for initial load
    teams = sorted(list(TEAM_DATA.keys()))
    products = get_available_products()
    
    # If no filters provided, just return the filter options
    if not filters:
        return {
            "skillData": [],
            "filterOptions": {
                "teams": teams,
                "products": products
            }
        }
    
    # Default to first team if no team specified
    if 'team' not in filters or not filters['team']:
        if teams:
            filters['team'] = teams[0]
    
    # Default to first product if no product specified
    if 'product' not in filters or not filters['product']:
        if products:
            filters['product'] = products[0]
    
    team = filters.get('team')
    product = filters.get('product')
    
    # Get the team's data
    team_data = get_team_data(team, product)
    if not team_data:
        return {
            "skillData": [],
            "filterOptions": {
                "teams": teams,
                "products": products
            }
        }
    
    # Calculate dynamic industry benchmarks
    industry_benchmarks = calculate_industry_benchmarks(team, product)
    
    skill_data = [
        {"subject": "Fluency", "teamAvg": team_data["skills"]["Fluency"], 
         "benchmark": industry_benchmarks["skills"]["Fluency"]},
        {"subject": "Introduction", "teamAvg": team_data["skills"]["Introduction"], 
         "benchmark": industry_benchmarks["skills"]["Introduction"]},
        {"subject": "Rapport", "teamAvg": team_data["skills"]["Rapport"], 
         "benchmark": industry_benchmarks["skills"]["Rapport"]},
        {"subject": "Interest", "teamAvg": team_data["skills"]["Interest"], 
         "benchmark": industry_benchmarks["skills"]["Interest"]},
        {"subject": "Probing", "teamAvg": team_data["skills"]["Probing"], 
         "benchmark": industry_benchmarks["skills"]["Probing"]},
        {"subject": "Product", "teamAvg": team_data["skills"]["Product"], 
         "benchmark": industry_benchmarks["skills"]["Product"]}
    ]
    
    return {
        "skillData": skill_data,
        "filterOptions": {
            "teams": teams,
            "products": products
        }
    }

def get_industry_benchmarks(filters=None):
    # Get teams list for initial load
    teams = sorted(list(TEAM_DATA.keys()))
    products = get_available_products()
    
    # If no filters provided, just return the filter options
    if not filters:
        return {
            "benchmarkData": [],
            "filterOptions": {
                "teams": teams,
                "products": products
            }
        }
    
    # Default to first team if no team specified
    if 'team' not in filters or not filters['team']:
        if teams:
            filters['team'] = teams[0]
    
    # Default to first product if no product specified
    if 'product' not in filters or not filters['product']:
        if products:
            filters['product'] = products[0]
    
    team = filters.get('team')
    product = filters.get('product')
    
    # Get the team's data
    team_data = get_team_data(team, product)
    if not team_data:
        return {
            "benchmarkData": [],
            "filterOptions": {
                "teams": teams,
                "products": products
            }
        }
    
    # Calculate dynamic industry benchmarks
    industry_benchmarks = calculate_industry_benchmarks(team, product)
    
    benchmark_data = [
        {"metric": "Overall Score", 
         "industryBenchmark": f"{industry_benchmarks['overall']}%", 
         "teamAverage": f"{team_data['overallScore']}%", 
         "difference": f"{'+' if team_data['overallScore'] - industry_benchmarks['overall'] >= 0 else ''}{team_data['overallScore'] - industry_benchmarks['overall']}%"},
        {"metric": "Fluency", 
         "industryBenchmark": f"{industry_benchmarks['skills']['Fluency']}%", 
         "teamAverage": f"{team_data['skills']['Fluency']}%", 
         "difference": f"{'+' if team_data['skills']['Fluency'] - industry_benchmarks['skills']['Fluency'] >= 0 else ''}{team_data['skills']['Fluency'] - industry_benchmarks['skills']['Fluency']}%"},
        {"metric": "Introduction", 
         "industryBenchmark": f"{industry_benchmarks['skills']['Introduction']}%", 
         "teamAverage": f"{team_data['skills']['Introduction']}%", 
         "difference": f"{'+' if team_data['skills']['Introduction'] - industry_benchmarks['skills']['Introduction'] >= 0 else ''}{team_data['skills']['Introduction'] - industry_benchmarks['skills']['Introduction']}%"},
        {"metric": "Rapport", 
         "industryBenchmark": f"{industry_benchmarks['skills']['Rapport']}%", 
         "teamAverage": f"{team_data['skills']['Rapport']}%", 
         "difference": f"{'+' if team_data['skills']['Rapport'] - industry_benchmarks['skills']['Rapport'] >= 0 else ''}{team_data['skills']['Rapport'] - industry_benchmarks['skills']['Rapport']}%"},
        {"metric": "Creating Interest", 
         "industryBenchmark": f"{industry_benchmarks['skills']['Interest']}%", 
         "teamAverage": f"{team_data['skills']['Interest']}%", 
         "difference": f"{'+' if team_data['skills']['Interest'] - industry_benchmarks['skills']['Interest'] >= 0 else ''}{team_data['skills']['Interest'] - industry_benchmarks['skills']['Interest']}%"},
        {"metric": "Probing", 
         "industryBenchmark": f"{industry_benchmarks['skills']['Probing']}%", 
         "teamAverage": f"{team_data['skills']['Probing']}%", 
         "difference": f"{'+' if team_data['skills']['Probing'] - industry_benchmarks['skills']['Probing'] >= 0 else ''}{team_data['skills']['Probing'] - industry_benchmarks['skills']['Probing']}%"},
        {"metric": "Product Knowledge", 
         "industryBenchmark": f"{industry_benchmarks['skills']['Product']}%", 
         "teamAverage": f"{team_data['skills']['Product']}%", 
         "difference": f"{'+' if team_data['skills']['Product'] - industry_benchmarks['skills']['Product'] >= 0 else ''}{team_data['skills']['Product'] - industry_benchmarks['skills']['Product']}%"}
    ]
    
    return {
        "benchmarkData": benchmark_data,
        "filterOptions": {
            "teams": teams,
            "products": products
        }
    }

def get_adoption_benchmarks(filters=None):
    # Get teams list for initial load
    teams = sorted(list(TEAM_DATA.keys()))
    products = get_available_products()
    
    # If no filters provided, just return the filter options
    if not filters:
        return {
            "adoptionData": [],
            "filterOptions": {
                "teams": teams,
                "products": products
            }
        }
    
    # Default to first team if no team specified
    if 'team' not in filters or not filters['team']:
        if teams:
            filters['team'] = teams[0]
    
    # Default to first product if no product specified
    if 'product' not in filters or not filters['product']:
        if products:
            filters['product'] = products[0]
    
    team = filters.get('team')
    product = filters.get('product')
    
    # Get the team's data
    team_data = get_team_data(team, product)
    if not team_data:
        return {
            "adoptionData": [],
            "filterOptions": {
                "teams": teams,
                "products": products
            }
        }
    
    # Calculate dynamic industry benchmarks
    industry_benchmarks = calculate_industry_benchmarks(team, product)
    
    adoption_data = [
        {"type": "Naive", 
         "industryBenchmark": f"{industry_benchmarks['adoption']['Naive']}%", 
         "teamAverage": f"{team_data['adoption']['Naive']}%", 
         "difference": f"{'+' if team_data['adoption']['Naive'] - industry_benchmarks['adoption']['Naive'] >= 0 else ''}{team_data['adoption']['Naive'] - industry_benchmarks['adoption']['Naive']}%"},
        {"type": "Passive", 
         "industryBenchmark": f"{industry_benchmarks['adoption']['Passive']}%", 
         "teamAverage": f"{team_data['adoption']['Passive']}%", 
         "difference": f"{'+' if team_data['adoption']['Passive'] - industry_benchmarks['adoption']['Passive'] >= 0 else ''}{team_data['adoption']['Passive'] - industry_benchmarks['adoption']['Passive']}%"},
        {"type": "Evaluator", 
         "industryBenchmark": f"{industry_benchmarks['adoption']['Evaluator']}%", 
         "teamAverage": f"{team_data['adoption']['Evaluator']}%", 
         "difference": f"{'+' if team_data['adoption']['Evaluator'] - industry_benchmarks['adoption']['Evaluator'] >= 0 else ''}{team_data['adoption']['Evaluator'] - industry_benchmarks['adoption']['Evaluator']}%"},
        {"type": "Adopter", 
         "industryBenchmark": f"{industry_benchmarks['adoption']['Adopter']}%", 
         "teamAverage": f"{team_data['adoption']['Adopter']}%", 
         "difference": f"{'+' if team_data['adoption']['Adopter'] - industry_benchmarks['adoption']['Adopter'] >= 0 else ''}{team_data['adoption']['Adopter'] - industry_benchmarks['adoption']['Adopter']}%"},
        {"type": "Advocate", 
         "industryBenchmark": f"{industry_benchmarks['adoption']['Advocate']}%", 
         "teamAverage": f"{team_data['adoption']['Advocate']}%", 
         "difference": f"{'+' if team_data['adoption']['Advocate'] - industry_benchmarks['adoption']['Advocate'] >= 0 else ''}{team_data['adoption']['Advocate'] - industry_benchmarks['adoption']['Advocate']}%"}
    ]
    
    return {
        "adoptionData": adoption_data,
        "filterOptions": {
            "teams": teams,
            "products": products
        }
    }

def get_situation_benchmarks(filters=None):
    # Get teams list for initial load
    teams = sorted(list(TEAM_DATA.keys()))
    products = get_available_products()
    
    # If no filters provided, just return the filter options
    if not filters:
        return {
            "situationData": [],
            "filterOptions": {
                "teams": teams,
                "products": products
            }
        }
    
    # Default to first team if no team specified
    if 'team' not in filters or not filters['team']:
        if teams:
            filters['team'] = teams[0]
    
    # Default to first product if no product specified
    if 'product' not in filters or not filters['product']:
        if products:
            filters['product'] = products[0]
    
    team = filters.get('team')
    product = filters.get('product')
    
    # Get the team's data
    team_data = get_team_data(team, product)
    if not team_data:
        return {
            "situationData": [],
            "filterOptions": {
                "teams": teams,
                "products": products
            }
        }
    
    # Calculate dynamic industry benchmarks
    industry_benchmarks = calculate_industry_benchmarks(team, product)
    
    situation_data = [
        {"situation": "Counter Call", 
         "industryBenchmark": f"{industry_benchmarks['situation']['Counter Call']}%", 
         "teamAverage": f"{team_data['situation']['Counter Call']}%", 
         "difference": f"{'+' if team_data['situation']['Counter Call'] - industry_benchmarks['situation']['Counter Call'] >= 0 else ''}{team_data['situation']['Counter Call'] - industry_benchmarks['situation']['Counter Call']}%"},
        {"situation": "Appointment", 
         "industryBenchmark": f"{industry_benchmarks['situation']['Appointment']}%", 
         "teamAverage": f"{team_data['situation']['Appointment']}%", 
         "difference": f"{'+' if team_data['situation']['Appointment'] - industry_benchmarks['situation']['Appointment'] >= 0 else ''}{team_data['situation']['Appointment'] - industry_benchmarks['situation']['Appointment']}%"},
        {"situation": "Lunch & Learn", 
         "industryBenchmark": f"{industry_benchmarks['situation']['Lunch & Learn']}%", 
         "teamAverage": f"{team_data['situation']['Lunch & Learn']}%", 
         "difference": f"{'+' if team_data['situation']['Lunch & Learn'] - industry_benchmarks['situation']['Lunch & Learn'] >= 0 else ''}{team_data['situation']['Lunch & Learn'] - industry_benchmarks['situation']['Lunch & Learn']}%"}
    ]
    
    return {
        "situationData": situation_data,
        "filterOptions": {
            "teams": teams,
            "products": products
        }
    }

# Route dictionary mapping paths to their respective handler functions
ROUTES = {
    '/industry-benchmarks': get_skill_comparison,
    '/industry-benchmarks/detail': get_industry_benchmarks,
    '/industry-benchmarks/adoption': get_adoption_benchmarks,
    '/industry-benchmarks/situation': get_situation_benchmarks
}

def lambda_handler(event, context):
    # Get the path from the event
    path = event.get('path', '')
    
    # Get query parameters for filtering
    query_params = event.get('queryStringParameters', {}) or {}
    filters = {}
    
    if 'team' in query_params:
        filters['team'] = query_params['team']
    
    if 'product' in query_params:
        filters['product'] = query_params['product']
    
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