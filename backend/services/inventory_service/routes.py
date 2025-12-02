from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.shared.database import get_db
from backend.shared import auth
from . import crud, schemas

router = APIRouter()

@router.post("/", response_model=schemas.Inventory)
async def create_inventory_item(
    inventory: schemas.InventoryCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    return await crud.create_inventory(db=db, inventory=inventory)

@router.get("/", response_model=list[schemas.Inventory])
async def read_all_inventory(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all inventory items (unauthenticated for chatbot access)"""
    return await crud.get_all_inventory(db, skip=skip, limit=limit)


@router.get("/{product_id}", response_model=schemas.Inventory)
async def read_inventory(
    product_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    db_inventory = await crud.get_inventory(db, product_id=product_id)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return db_inventory

@router.put("/{product_id}/stock", response_model=schemas.Inventory)
async def update_stock(
    product_id: int, 
    stock_update: schemas.InventoryUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    db_inventory = await crud.update_stock(db, product_id=product_id, quantity_change=stock_update.quantity)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return db_inventory
