import json

def handle_benchmarks_request(event, context):
    path = event.get('path', '')
    
    # Remove leading slash if present
    path = path.lstrip('/')
    
    # Debug logging
    print(f"Benchmarks handler received path: {path}")
    
    # Base benchmarks data with filter options
    benchmarks_data = {
        "filterOptions": {
            "teams": ["North Region", "South Region", "East Region", "West Region"],
            "products": ["Product A", "Product B", "Product C", "Product D"]
        },
        "skillData": [
            {
                "subject": "Overall Score",
                "teamAvg": 75,
                "benchmark": 70
            },
            {
                "subject": "Fluency",
                "teamAvg": 78,
                "benchmark": 72
            },
            {
                "subject": "Introduction",
                "teamAvg": 82,
                "benchmark": 75
            },
            {
                "subject": "Rapport",
                "teamAvg": 70,
                "benchmark": 65
            },
            {
                "subject": "Interest",
                "teamAvg": 80,
                "benchmark": 73
            },
            {
                "subject": "Probing",
                "teamAvg": 75,
                "benchmark": 70
            },
            {
                "subject": "Product",
                "teamAvg": 72,
                "benchmark": 68
            }
        ],
        "benchmarkData": [
            {
                "metric": "Overall Score",
                "teamAverage": 75,
                "industryBenchmark": 70,
                "difference": "+5%"
            },
            {
                "metric": "Simulations Completed",
                "teamAverage": 82,
                "industryBenchmark": 75,
                "difference": "+7%"
            },
            {
                "metric": "Improvement Rate",
                "teamAverage": 15,
                "industryBenchmark": 12,
                "difference": "+3%"
            }
        ],
        "adoptionData": [
            {
                "type": "Passive",
                "teamAverage": 20,
                "industryBenchmark": 25,
                "difference": "-5%"
            },
            {
                "type": "Evaluator",
                "teamAverage": 35,
                "industryBenchmark": 40,
                "difference": "-5%"
            },
            {
                "type": "Adopter",
                "teamAverage": 30,
                "industryBenchmark": 25,
                "difference": "+5%"
            },
            {
                "type": "Advocate",
                "teamAverage": 15,
                "industryBenchmark": 10,
                "difference": "+5%"
            }
        ],
        "situationData": [
            {
                "situation": "Appointment",
                "teamAverage": 45,
                "industryBenchmark": 40,
                "difference": "+5%"
            },
            {
                "situation": "Counter Call",
                "teamAverage": 25,
                "industryBenchmark": 30,
                "difference": "-5%"
            },
            {
                "situation": "Lunch & Learn",
                "teamAverage": 20,
                "industryBenchmark": 20,
                "difference": "0%"
            },
            {
                "situation": "Other",
                "teamAverage": 10,
                "industryBenchmark": 10,
                "difference": "0%"
            }
        ]
    }

    # Handle different endpoints
    if path == 'industry-benchmarks':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "skillData": benchmarks_data["skillData"],
                "filterOptions": benchmarks_data["filterOptions"]
            })
        }
    elif path == 'industry-benchmarks/detail':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "benchmarkData": benchmarks_data["benchmarkData"]
            })
        }
    elif path == 'industry-benchmarks/adoption':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "adoptionData": benchmarks_data["adoptionData"]
            })
        }
    elif path == 'industry-benchmarks/situation':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            "body": json.dumps({
                "situationData": benchmarks_data["situationData"]
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
