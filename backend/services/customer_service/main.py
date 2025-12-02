from fastapi import FastAPI
from backend.services.customer_service import routes, models
from backend.shared.database import engine
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield

app = FastAPI(title="Customer Service", lifespan=lifespan)

app.include_router(routes.router, prefix="/api/tickets", tags=["tickets"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
