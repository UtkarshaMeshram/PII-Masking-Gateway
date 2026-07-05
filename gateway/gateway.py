from fastapi import FastAPI, Request, Response
import requests

app = FastAPI()

TARGET_SERVER = "http://localhost:3000"

@app.api_route("/{path:path}", methods=["GET","POST","PUT","DELETE"])
async def proxy(request: Request, path: str):

    url = f"{TARGET_SERVER}/{path}"

    body = await request.body()

    response = requests.request(
        method=request.method,
        url=url,
        headers=dict(request.headers),
        data=body,
        allow_redirects=False
    )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers)
    )