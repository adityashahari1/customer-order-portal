from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.shared.database import get_db
from backend.shared import auth
from . import crud, schemas, models

router = APIRouter()

@router.post("/", response_model=schemas.Return)
async def create_return_request(
    return_req: schemas.ReturnCreate, 
    db: AsyncSession = Depends(get_db)
    # Removed auth for demo/chatbot integration
):
    return await crud.create_return(db=db, return_req=return_req)

@router.get("/", response_model=list[schemas.Return])
async def read_all_returns(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all return requests (unauthenticated for frontend access)"""
    return await crud.get_all_returns(db, skip=skip, limit=limit)


@router.get("/{return_id}", response_model=schemas.Return)
async def read_return(
    return_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    db_return = await crud.get_return(db, return_id=return_id)
    if db_return is None:
        raise HTTPException(status_code=404, detail="Return request not found")
    return db_return

@router.put("/{return_id}/status", response_model=schemas.Return)
async def update_return_status(
    return_id: int, 
    status_update: schemas.ReturnUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    db_return = await crud.update_return_status(db, return_id=return_id, status=status_update.status.value)
    if db_return is None:
        raise HTTPException(status_code=404, detail="Return request not found")
    return db_return
