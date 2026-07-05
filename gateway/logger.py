import json
from datetime import datetime

LOG_FILE = "pii_logs.txt"

def log_event(input_text, detected, masked, risk_score):
    log_entry = {
        "timestamp": str(datetime.now()),
        "input": input_text,
        "detected": detected,
        "masked": masked,
        "risk_score": risk_score
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")