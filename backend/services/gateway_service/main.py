import httpx
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERVICES = {
    "orders": "http://localhost:8001",
    "returns": "http://localhost:8002",
    "inventory": "http://localhost:8003",
    "tickets": "http://localhost:8004",
    "chatbot": "http://localhost:8005",
    "salesforce": "http://localhost:8006",
    "notifications": "http://localhost:8007",
    "analytics": "http://localhost:8008",
}

@app.api_route("/api/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(service: str, path: str, request: Request):
    if service not in SERVICES:
        return Response(content="Service not found", status_code=404)

    url = f"{SERVICES[service]}/api/{service}/{path}"
    
    # Forward query params
    params = dict(request.query_params)
    
    # Increase timeout for AI services
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            # Forward body if present
            body = await request.body()
            
            response = await client.request(
                method=request.method,
                url=url,
                content=body,
                params=params,
                headers=request.headers.raw
            )
            
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except Exception as e:
            return Response(content=str(e), status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
