import json
import datetime
import os

FILE_PATH = "incidents.json"


def save_incident(original, masked, detected, score, level):
    # ---------------- CREATE INCIDENT ----------------
    incident = {
        "time": str(datetime.datetime.now()),
        "original_text": original,
        "masked_text": masked,
        "pii_detected": detected,
        "risk_score": score,
        "risk_level": level
    }

    # ---------------- LOAD EXISTING DATA ----------------
    if not os.path.exists(FILE_PATH):
        data = []
    else:
        try:
            with open(FILE_PATH, "r") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = []
        except Exception as e:
            print("Error reading file:", e)
            data = []

    # ---------------- APPEND NEW INCIDENT ----------------
    data.append(incident)

    # ---------------- SAVE BACK ----------------
    try:
        with open(FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print("Error saving incident:", e)