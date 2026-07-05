import re

def detect_pii(text):

    patterns ={
        "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",

        "phone": r"\b\d{10}\b",

        "aadhaar": r"\b\d{4}\s?\d{4}\s?\d{4}\b",

        "pan": r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",

        "credit_card": r"\b\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b",
        
        "cvv": r"(?:CVV|cvv)[^\d]*(\d{3})"
    }
    

    results = {}

    for key, pattern in patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            results[key] = matches

    return results