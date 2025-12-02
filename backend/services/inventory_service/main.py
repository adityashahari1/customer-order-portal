from fastapi import FastAPI
from backend.services.inventory_service import routes, models
from backend.shared.database import engine
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield

app = FastAPI(title="Inventory Service", lifespan=lifespan)

app.include_router(routes.router, prefix="/api/inventory", tags=["inventory"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
