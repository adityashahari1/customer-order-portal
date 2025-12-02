from fastapi import FastAPI
from backend.services.analytics_service import routes

app = FastAPI(title="Analytics Service")

app.include_router(routes.router, prefix="/api/analytics", tags=["analytics"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008)
