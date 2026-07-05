def calculate_risk(pii_data):
    
    score = 0

    weights = {
        "email": 10,
        "phone": 15,
        "pan": 40,
        "credit_card": 50,
        "aadhaar": 60,
        "cvv": 40
    } 

    for key in pii_data:
        score += weights.get(key, 5)

    if score >= 70:
        level = "HIGH"
    elif score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level