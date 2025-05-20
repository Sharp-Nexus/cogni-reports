import json

def lambda_handler(event, context):
    query_params = event.get('queryStringParameters', {}) or {}
    product_filter = query_params.get('product')
    specialty_filter = query_params.get('specialty')
    
    simulation_data = [
        {
            "id": 1,
            "date": "April 8, 2025",
            "adoptionLevel": "Passive",
            "situation": "Appointment",
            "product": "Besophil",
            "specialty": "Cardiology",
            "overallScore": 48,
            "fluency": 42,
            "introduction": 65,
            "rapport": 35,
            "interest": 60,
            "probing": 45,
            "productKnowledge": 40
        },
        {
            "id": 2,
            "date": "April 8, 2025",
            "adoptionLevel": "Passive",
            "situation": "Counter Call",
            "product": "ELF",
            "specialty": "Oncology",
            "overallScore": 55,
            "fluency": 50,
            "introduction": 75,
            "rapport": 40,
            "interest": 65,
            "probing": 55,
            "productKnowledge": 45
        },
        {
            "id": 3,
            "date": "April 8, 2025",
            "adoptionLevel": "Evaluator",
            "situation": "Appointment",
            "product": "Besophil",
            "specialty": "Neurology",
            "overallScore": 62,
            "fluency": 58,
            "introduction": 80,
            "rapport": 50,
            "interest": 70,
            "probing": 65,
            "productKnowledge": 50
        },
        {
            "id": 4,
            "date": "April 8, 2025",
            "adoptionLevel": "Adopter",
            "situation": "Appointment",
            "product": "ELF",
            "specialty": "Cardiology",
            "overallScore": 72,
            "fluency": 68,
            "introduction": 85,
            "rapport": 65,
            "interest": 80,
            "probing": 75,
            "productKnowledge": 60
        },
        {
            "id": 5,
            "date": "April 8, 2025",
            "adoptionLevel": "Advocate",
            "situation": "Lunch & Learn",
            "product": "Besophil",
            "specialty": "Oncology",
            "overallScore": 85,
            "fluency": 82,
            "introduction": 90,
            "rapport": 80,
            "interest": 90,
            "probing": 85,
            "productKnowledge": 85
        }
    ]

    # Apply filters
    filtered_data = simulation_data
    if product_filter and product_filter != 'all':
        filtered_data = [item for item in filtered_data if item['product'] == product_filter]
    if specialty_filter and specialty_filter != 'all':
        filtered_data = [item for item in filtered_data if item['specialty'] == specialty_filter]

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*"
        },
        "body": json.dumps({
            "simulationData": filtered_data
        }),
    } 
