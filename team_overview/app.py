import json

# Base data structure for all teams and products
BASE_DATA = {
    "Team A": {
        "Besophil": {
            "overall": 78,
            "simulations": 70,
            "improvement": 20,
            "comparison": {
                "Fluency": {"team": 80, "average": 72},
                "Introduction": {"team": 79, "average": 68},
                "Rapport": {"team": 82, "average": 70},
                "Interest": {"team": 77, "average": 69},
                "Probing": {"team": 75, "average": 71},
                "Product": {"team": 81, "average": 73}
            },
            "trend": [
                {"name": "Week 1", "team": 62, "industry": 70},
                {"name": "Week 2", "team": 67, "industry": 70},
                {"name": "Week 3", "team": 72, "industry": 70},
                {"name": "Week 4", "team": 75, "industry": 70},
                {"name": "Week 5", "team": 77, "industry": 70},
                {"name": "Week 6", "team": 78, "industry": 70}
            ],
            "adoption": {
                "Naive": 68,
                "Evaluator": 82,
                "Advocate": 80
            },
            "situation": {
                "Counter Call": 75,
                "Appointment": 80,
                "Lunch & Learn": 78
            }
        },
        "ELF": {
            "overall": 75,
            "simulations": 65,
            "improvement": 18,
            "comparison": {
                "Fluency": {"team": 77, "average": 72},
                "Introduction": {"team": 74, "average": 68},
                "Rapport": {"team": 76, "average": 70},
                "Interest": {"team": 73, "average": 69},
                "Probing": {"team": 72, "average": 71},
                "Product": {"team": 78, "average": 73}
            },
            "trend": [
                {"name": "Week 1", "team": 60, "industry": 70},
                {"name": "Week 2", "team": 65, "industry": 70},
                {"name": "Week 3", "team": 70, "industry": 70},
                {"name": "Week 4", "team": 72, "industry": 70},
                {"name": "Week 5", "team": 74, "industry": 70},
                {"name": "Week 6", "team": 75, "industry": 70}
            ],
            "adoption": {
                "Naive": 66,
                "Evaluator": 77,
                "Advocate": 75
            },
            "situation": {
                "Counter Call": 73,
                "Appointment": 76,
                "Lunch & Learn": 75
            }
        }
    },
    "Team B": {
        "Besophil": {
            "overall": 74,
            "simulations": 62,
            "improvement": 15,
            "comparison": {
                "Fluency": {"team": 75, "average": 72},
                "Introduction": {"team": 72, "average": 68},
                "Rapport": {"team": 76, "average": 70},
                "Interest": {"team": 73, "average": 69},
                "Probing": {"team": 71, "average": 71},
                "Product": {"team": 77, "average": 73}
            },
            "trend": [
                {"name": "Week 1", "team": 65, "industry": 70},
                {"name": "Week 2", "team": 68, "industry": 70},
                {"name": "Week 3", "team": 70, "industry": 70},
                {"name": "Week 4", "team": 72, "industry": 70},
                {"name": "Week 5", "team": 73, "industry": 70},
                {"name": "Week 6", "team": 74, "industry": 70}
            ],
            "adoption": {
                "Naive": 66,
                "Evaluator": 78,
                "Advocate": 75
            },
            "situation": {
                "Counter Call": 73,
                "Appointment": 76,
                "Lunch & Learn": 74
            }
        },
        "ELF": {
            "overall": 71,
            "simulations": 58,
            "improvement": 12,
            "comparison": {
                "Fluency": {"team": 73, "average": 72},
                "Introduction": {"team": 69, "average": 68},
                "Rapport": {"team": 72, "average": 70},
                "Interest": {"team": 70, "average": 69},
                "Probing": {"team": 68, "average": 71},
                "Product": {"team": 74, "average": 73}
            },
            "trend": [
                {"name": "Week 1", "team": 63, "industry": 70},
                {"name": "Week 2", "team": 66, "industry": 70},
                {"name": "Week 3", "team": 68, "industry": 70},
                {"name": "Week 4", "team": 70, "industry": 70},
                {"name": "Week 5", "team": 71, "industry": 70},
                {"name": "Week 6", "team": 71, "industry": 70}
            ],
            "adoption": {
                "Naive": 64,
                "Evaluator": 74,
                "Advocate": 72
            },
            "situation": {
                "Counter Call": 71,
                "Appointment": 73,
                "Lunch & Learn": 72
            }
        }
    },
    "Team C": {
        "Besophil": {
            "overall": 71,
            "simulations": 56,
            "improvement": 8,
            "comparison": {
                "Fluency": {"team": 72, "average": 72},
                "Introduction": {"team": 68, "average": 68},
                "Rapport": {"team": 73, "average": 70},
                "Interest": {"team": 70, "average": 69},
                "Probing": {"team": 69, "average": 71},
                "Product": {"team": 74, "average": 73}
            },
            "trend": [
                {"name": "Week 1", "team": 68, "industry": 70},
                {"name": "Week 2", "team": 69, "industry": 70},
                {"name": "Week 3", "team": 70, "industry": 70},
                {"name": "Week 4", "team": 70, "industry": 70},
                {"name": "Week 5", "team": 71, "industry": 70},
                {"name": "Week 6", "team": 71, "industry": 70}
            ],
            "adoption": {
                "Naive": 64,
                "Evaluator": 73,
                "Advocate": 72
            },
            "situation": {
                "Counter Call": 70,
                "Appointment": 73,
                "Lunch & Learn": 71
            }
        },
        "ELF": {
            "overall": 68,
            "simulations": 52,
            "improvement": 5,
            "comparison": {
                "Fluency": {"team": 70, "average": 72},
                "Introduction": {"team": 66, "average": 68},
                "Rapport": {"team": 69, "average": 70},
                "Interest": {"team": 67, "average": 69},
                "Probing": {"team": 65, "average": 71},
                "Product": {"team": 71, "average": 73}
            },
            "trend": [
                {"name": "Week 1", "team": 66, "industry": 70},
                {"name": "Week 2", "team": 67, "industry": 70},
                {"name": "Week 3", "team": 68, "industry": 70},
                {"name": "Week 4", "team": 68, "industry": 70},
                {"name": "Week 5", "team": 68, "industry": 70},
                {"name": "Week 6", "team": 68, "industry": 70}
            ],
            "adoption": {
                "Naive": 62,
                "Evaluator": 70,
                "Advocate": 69
            },
            "situation": {
                "Counter Call": 68,
                "Appointment": 70,
                "Lunch & Learn": 69
            }
        }
    }
}

def get_team_averages(filters=None):
    data = {
        "teamAverages": {
            "overall": 73,
            "simulations": 59,
            "improvement": 15
        },
        "industryBenchmarks": {
            "overall": 70
        }
    }
    
    if filters:
        product = filters.get('product')
        team = filters.get('team')
        
        if team and team != 'all' and product and product != 'all':
            # Get specific team and product data
            team_data = BASE_DATA[team][product]
            data['teamAverages'] = {
                "overall": team_data['overall'],
                "simulations": team_data['simulations'],
                "improvement": team_data['improvement']
            }
        elif team and team != 'all':
            # Get team data averaged across all products
            team_data = BASE_DATA[team]
            overall = sum(p['overall'] for p in team_data.values()) / len(team_data)
            simulations = sum(p['simulations'] for p in team_data.values()) / len(team_data)
            improvement = sum(p['improvement'] for p in team_data.values()) / len(team_data)
            data['teamAverages'] = {
                "overall": round(overall),
                "simulations": round(simulations),
                "improvement": round(improvement)
            }
        elif product and product != 'all':
            # Get product data averaged across all teams
            product_data = {team: data[product] for team, data in BASE_DATA.items()}
            overall = sum(p['overall'] for p in product_data.values()) / len(product_data)
            simulations = sum(p['simulations'] for p in product_data.values()) / len(product_data)
            improvement = sum(p['improvement'] for p in product_data.values()) / len(product_data)
            data['teamAverages'] = {
                "overall": round(overall),
                "simulations": round(simulations),
                "improvement": round(improvement)
            }
    
    return data

def get_team_comparison(filters=None):
    # Define all metrics
    metric_names = [
        "Overall", "Fluency", "Introduction", "Rapport", "Interest", "Probing", "Product"
    ]

    # Calculate product-specific averages for each metric
    product_metrics = {"Besophil": {}, "ELF": {}}
    
    # For each product, calculate the average across all teams for each metric
    for product_name in product_metrics:
        product_metrics[product_name] = {name: [] for name in metric_names}
        
        for team_data in BASE_DATA.values():
            if product_name in team_data:
                # Add overall metric
                product_metrics[product_name]["Overall"].append(team_data[product_name].get("overall", 0))
                
                # Add other metrics if available
                if "comparison" in team_data[product_name]:
                    for metric in metric_names:
                        if metric != "Overall":
                            product_metrics[product_name][metric].append(
                                team_data[product_name]["comparison"].get(metric, {}).get("team", 0)
                            )
    
    # Calculate the averages for each product and metric
    product_averages = {}
    for product_name, metrics in product_metrics.items():
        product_averages[product_name] = {}
        for metric, values in metrics.items():
            product_averages[product_name][metric] = round(sum(values) / len(values)) if values else 0
    
    # Calculate overall metrics average across all teams and products
    all_metrics = {name: [] for name in metric_names}
    for team in BASE_DATA.values():
        for product in team.values():
            all_metrics["Overall"].append(product.get("overall", 0))
            if "comparison" in product:
                for metric in metric_names:
                    if metric != "Overall":
                        all_metrics[metric].append(product["comparison"].get(metric, {}).get("team", 0))

    overall_averages = {
        metric: round(sum(values) / len(values)) if values else 0
        for metric, values in all_metrics.items()
    }

    # Default data - show overall averages for all metrics
    data = {
        "teamComparisonData": [
            {"name": metric, "team": overall_averages[metric], "average": overall_averages[metric]}
            for metric in metric_names
        ]
    }

    if filters:
        product = filters.get('product')
        team = filters.get('team')

        if team and team != 'all' and product and product != 'all':
            # Get specific team and product comparison
            team_data = BASE_DATA[team][product]
            team_metrics = {}
            
            # Overall metric
            team_metrics["Overall"] = team_data.get("overall", 0)
            
            # Other metrics
            if "comparison" in team_data:
                for metric in metric_names:
                    if metric != "Overall":
                        team_metrics[metric] = team_data["comparison"].get(metric, {}).get("team", 0)
            
            # Fill missing metrics with 0
            for metric in metric_names:
                if metric not in team_metrics:
                    team_metrics[metric] = 0
            
            # Use product-specific averages for comparison
            data['teamComparisonData'] = [
                {"name": metric, "team": team_metrics[metric], "average": product_averages[product][metric]}
                for metric in metric_names
            ]
        elif team and team != 'all':
            # Get team comparison averaged across all products
            team_data = BASE_DATA[team]
            team_metrics = {name: [] for name in metric_names}
            
            for product_name, product_data in team_data.items():
                team_metrics["Overall"].append(product_data.get("overall", 0))
                if "comparison" in product_data:
                    for metric in metric_names:
                        if metric != "Overall":
                            team_metrics[metric].append(product_data["comparison"].get(metric, {}).get("team", 0))
            
            team_averages = {
                metric: round(sum(values) / len(values)) if values else 0
                for metric, values in team_metrics.items()
            }
            
            # Compare with overall averages
            data['teamComparisonData'] = [
                {"name": metric, "team": team_averages[metric], "average": overall_averages[metric]}
                for metric in metric_names
            ]
        elif product and product != 'all':
            # Get product comparison averaged across all teams
            product_data = []
            for team_name, team_data in BASE_DATA.items():
                if product in team_data:
                    # Add this team's product data
                    team_product_data = {"team": team_name}
                    
                    # Overall metric
                    team_product_data["Overall"] = team_data[product].get("overall", 0)
                    
                    # Other metrics
                    if "comparison" in team_data[product]:
                        for metric in metric_names:
                            if metric != "Overall":
                                team_product_data[metric] = team_data[product]["comparison"].get(metric, {}).get("team", 0)
                    
                    product_data.append(team_product_data)
            
            # Calculate average for each metric across teams for this product
            product_team_metrics = {name: [] for name in metric_names}
            for team_product in product_data:
                for metric in metric_names:
                    if metric in team_product:
                        product_team_metrics[metric].append(team_product[metric])
            
            product_team_averages = {
                metric: round(sum(values) / len(values)) if values else 0
                for metric, values in product_team_metrics.items()
            }
            
            # Use product-specific averages
            data['teamComparisonData'] = [
                {"name": metric, "team": product_team_averages[metric], "average": product_averages[product][metric]}
                for metric in metric_names
            ]

    return data

def get_team_trend(filters=None):
    data = {
        "teamTrendData": [
            {"name": "Week 1", "team": 65, "industry": 70},
            {"name": "Week 2", "team": 68, "industry": 70},
            {"name": "Week 3", "team": 70, "industry": 70},
            {"name": "Week 4", "team": 72, "industry": 70},
            {"name": "Week 5", "team": 73, "industry": 70},
            {"name": "Week 6", "team": 73, "industry": 70}
        ]
    }
    
    if filters:
        product = filters.get('product')
        team = filters.get('team')
        
        if team and team != 'all' and product and product != 'all':
            # Get specific team and product trend
            data['teamTrendData'] = BASE_DATA[team][product]['trend']
        elif team and team != 'all':
            # Get team trend averaged across all products
            team_trends = [BASE_DATA[team][p]['trend'] for p in BASE_DATA[team]]
            averaged_trend = []
            for week in range(6):
                week_data = {
                    "name": f"Week {week + 1}",
                    "team": round(sum(trend[week]['team'] for trend in team_trends) / len(team_trends)),
                    "industry": 70
                }
                averaged_trend.append(week_data)
            data['teamTrendData'] = averaged_trend
        elif product and product != 'all':
            # Get product trend averaged across all teams
            product_trends = [BASE_DATA[team][product]['trend'] for team in BASE_DATA]
            averaged_trend = []
            for week in range(6):
                week_data = {
                    "name": f"Week {week + 1}",
                    "team": round(sum(trend[week]['team'] for trend in product_trends) / len(product_trends)),
                    "industry": 70
                }
                averaged_trend.append(week_data)
            data['teamTrendData'] = averaged_trend
    
    return data

def get_team_adoption(filters=None):
    # Define adoption levels
    adoption_levels = ["Naive", "Evaluator", "Advocate"]
    
    # Calculate product-specific averages for each adoption level
    product_averages = {"Besophil": {}, "ELF": {}}
    
    for product_name in product_averages:
        product_averages[product_name] = {level: [] for level in adoption_levels}
        
        for team_data in BASE_DATA.values():
            if product_name in team_data:
                for level in adoption_levels:
                    product_averages[product_name][level].append(team_data[product_name]["adoption"][level])
        
        # Calculate averages
        for level in adoption_levels:
            values = product_averages[product_name][level]
            product_averages[product_name][level] = round(sum(values) / len(values)) if values else 0
    
    # Calculate overall averages across all teams and products
    overall_averages = {level: [] for level in adoption_levels}
    
    for team in BASE_DATA.values():
        for product_name, product in team.items():
            for level in adoption_levels:
                overall_averages[level].append(product["adoption"][level])
    
    # Calculate overall averages
    for level in overall_averages:
        values = overall_averages[level]
        overall_averages[level] = round(sum(values) / len(values)) if values else 0
    
    # Default data - overall averages
    data = {
        "adoptionData": [
            {"name": level, "team": overall_averages[level], "industry": overall_averages[level]}
            for level in adoption_levels
        ]
    }
    
    if filters:
        product = filters.get('product')
        team = filters.get('team')
        
        if team and team != 'all' and product and product != 'all':
            # Get specific team and product adoption data
            team_product_data = BASE_DATA[team][product]["adoption"]
            
            data['adoptionData'] = [
                {"name": level, "team": team_product_data[level], "industry": product_averages[product][level]}
                for level in adoption_levels
            ]
        elif team and team != 'all':
            # Get team data averaged across all products
            team_levels = {level: [] for level in adoption_levels}
            
            for product_data in BASE_DATA[team].values():
                for level in adoption_levels:
                    team_levels[level].append(product_data["adoption"][level])
            
            # Calculate team averages across products
            team_averages = {}
            for level, values in team_levels.items():
                team_averages[level] = round(sum(values) / len(values)) if values else 0
            
            data['adoptionData'] = [
                {"name": level, "team": team_averages[level], "industry": overall_averages[level]}
                for level in adoption_levels
            ]
        elif product and product != 'all':
            # Get product data averaged across all teams
            data['adoptionData'] = [
                {"name": level, "team": product_averages[product][level], "industry": product_averages[product][level]}
                for level in adoption_levels
            ]
    
    return data

def get_team_situation(filters=None):
    # Define situation types
    situation_types = ["Counter Call", "Appointment", "Lunch & Learn"]
    
    # Calculate product-specific averages for each situation type
    product_averages = {"Besophil": {}, "ELF": {}}
    
    for product_name in product_averages:
        product_averages[product_name] = {situation: [] for situation in situation_types}
        
        for team_data in BASE_DATA.values():
            if product_name in team_data:
                for situation in situation_types:
                    product_averages[product_name][situation].append(team_data[product_name]["situation"][situation])
        
        # Calculate averages
        for situation in situation_types:
            values = product_averages[product_name][situation]
            product_averages[product_name][situation] = round(sum(values) / len(values)) if values else 0
    
    # Calculate overall averages across all teams and products
    overall_averages = {situation: [] for situation in situation_types}
    
    for team in BASE_DATA.values():
        for product_name, product in team.items():
            for situation in situation_types:
                overall_averages[situation].append(product["situation"][situation])
    
    # Calculate overall averages
    for situation in overall_averages:
        values = overall_averages[situation]
        overall_averages[situation] = round(sum(values) / len(values)) if values else 0
    
    # Default data - overall averages
    data = {
        "situationData": [
            {"name": situation, "team": overall_averages[situation], "industry": overall_averages[situation]}
            for situation in situation_types
        ]
    }
    
    if filters:
        product = filters.get('product')
        team = filters.get('team')
        
        if team and team != 'all' and product and product != 'all':
            # Get specific team and product situation data
            team_product_data = BASE_DATA[team][product]["situation"]
            
            data['situationData'] = [
                {"name": situation, "team": team_product_data[situation], "industry": product_averages[product][situation]}
                for situation in situation_types
            ]
        elif team and team != 'all':
            # Get team data averaged across all products
            team_situations = {situation: [] for situation in situation_types}
            
            for product_data in BASE_DATA[team].values():
                for situation in situation_types:
                    team_situations[situation].append(product_data["situation"][situation])
            
            # Calculate team averages across products
            team_averages = {}
            for situation, values in team_situations.items():
                team_averages[situation] = round(sum(values) / len(values)) if values else 0
            
            data['situationData'] = [
                {"name": situation, "team": team_averages[situation], "industry": overall_averages[situation]}
                for situation in situation_types
            ]
        elif product and product != 'all':
            # Get product data averaged across all teams
            data['situationData'] = [
                {"name": situation, "team": product_averages[product][situation], "industry": product_averages[product][situation]}
                for situation in situation_types
            ]
    
    return data

def get_all_data(filters=None):
    return {
        **get_team_averages(filters),
        **get_team_comparison(filters),
        **get_team_trend(filters),
        **get_team_adoption(filters),
        **get_team_situation(filters)
    }

# Route dictionary mapping paths to their respective handler functions
ROUTES = {
    '/team-overview': get_all_data,
    '/team-overview/averages': get_team_averages,
    '/team-overview/comparison': get_team_comparison,
    '/team-overview/trend': get_team_trend,
    '/team-overview/adoption': get_team_adoption,
    '/team-overview/situation': get_team_situation
}

def lambda_handler(event, context):
    # Get the path from the event
    path = event.get('path', '')
    
    # Get query parameters for filtering
    query_params = event.get('queryStringParameters', {}) or {}
    filters = {}
    
    if 'product' in query_params:
        filters['product'] = query_params['product']
    if 'team' in query_params:
        filters['team'] = query_params['team']
    
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