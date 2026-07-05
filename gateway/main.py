from fastapi import FastAPI, File, UploadFile, Request, Response
from pydantic import BaseModel
from pii_detector import detect_pii
from logger import log_event
from masking import mask_pii
from risk_engine import calculate_risk
from incident_store import save_incident
import httpx
from datetime import datetime

app = FastAPI()

JUICE_SHOP_URL = "http://localhost:3000"


class TextInput(BaseModel):
    text: str


@app.post("/scan")
async def scan(data: TextInput):
    try:
        detected = detect_pii(data.text)

        if detected:
           masked = mask_pii(data.text, detected)
           score, level = calculate_risk(detected)

           log_event(data.text, detected, masked, score)
           save_incident(data.text, masked, detected, score, level)

        return {
    "status": "success",
    "pii_detected": detected,
    "masked_output": masked if detected else data.text,
    "risk_score": score if detected else 0,
    "risk_level": level if detected else "LOW"
}

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/logs")
def get_logs():
    try:
        with open("pii_logs.txt", "r", encoding="utf-8") as file:
            logs = file.readlines()
        return {"logs": logs}
    except FileNotFoundError:
        return {"message": "No logs found"}


@app.post("/scan-file")
async def scan_file(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")

    detected = detect_pii(text)
    masked = mask_pii(text, detected)
    log_event(text, detected)
    score, level = calculate_risk(detected)
    save_incident(text, masked, detected, score, level)

    if "aadhaar" in detected:
        return {
            "status": "BLOCKED",
            "reason": "Aadhaar number detected",
            "risk_score": score,
            "risk_level": level,
            "masked_output": masked
        }

    status = "WARNING" if detected else "SAFE"

    return {
        "file_name": file.filename,
        "pii_detected": detected,
        "masked_output": masked,
        "risk_score": score,
        "risk_level": level,
        "status": status
    }


# ✅ Root route (homepage)
@app.get("/")
async def root():
    async with httpx.AsyncClient() as client:
        response = await client.get(JUICE_SHOP_URL)

    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type=response.headers.get("content-type")
    )


# ✅ Proxy route (everything else)
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_to_juice_shop(path: str, request: Request):

    # Handle empty path
    target_url = f"{JUICE_SHOP_URL}/{path}" if path else JUICE_SHOP_URL

    body = await request.body()

    # Try PII detection safely
    try:
        text = body.decode("utf-8")
        detected = detect_pii(text)

        if detected:
            masked = mask_pii(text, detected)
            score, level = calculate_risk(detected)

            log_event(text, detected, masked, score)
            save_incident(text, masked, detected, score, level)

            # 🚨 Block Aadhaar
            if "aadhaar" in detected:
                return Response(
                    content='{"error": "Blocked due to Aadhaar"}',
                    media_type="application/json",
                    status_code=403
                )

            body = masked.encode()

    except:
        pass  # ignore binary files (VERY IMPORTANT)

    # Forward headers
    headers = dict(request.headers)
    headers.pop("host", None)

    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.request(
            method=request.method,
            url=target_url,
            params=request.query_params,
            content=body,
            headers=headers
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.headers.get("content-type")
    )