from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas

async def get_inventory(db: AsyncSession, product_id: int):
    result = await db.execute(select(models.Inventory).where(models.Inventory.product_id == product_id))
    return result.scalars().first()

async def get_all_inventory(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Inventory).offset(skip).limit(limit))
    return result.scalars().all()


async def create_inventory(db: AsyncSession, inventory: schemas.InventoryCreate):
    db_inventory = models.Inventory(**inventory.dict())
    db.add(db_inventory)
    await db.commit()
    await db.refresh(db_inventory)
    return db_inventory

async def update_stock(db: AsyncSession, product_id: int, quantity_change: int):
    db_inventory = await get_inventory(db, product_id)
    if db_inventory:
        db_inventory.quantity += quantity_change
        await db.commit()
        await db.refresh(db_inventory)
    return db_inventory
