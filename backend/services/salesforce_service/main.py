from fastapi import FastAPI
from backend.services.salesforce_service import routes

app = FastAPI(title="Salesforce Service")

app.include_router(routes.router, prefix="/api/salesforce", tags=["salesforce"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)
