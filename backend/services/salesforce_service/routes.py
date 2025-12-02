from fastapi import APIRouter, Depends
from backend.shared import auth
from backend.agents.salesforce_agent import sync_customer_data
from . import schemas

router = APIRouter()

@router.post("/sync")
async def sync_entity(
    request: schemas.SyncRequest, 
    current_user: dict = Depends(auth.get_current_user)
):
    result = sync_customer_data(request.data)
    return {"result": str(result)}
