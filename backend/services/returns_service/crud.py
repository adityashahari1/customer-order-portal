from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas

async def create_return(db: AsyncSession, return_req: schemas.ReturnCreate):
    db_return = models.Return(
        order_id=return_req.order_id,
        reason=return_req.reason,
        refund_amount=return_req.refund_amount,
        status=models.ReturnStatus.REQUESTED.value
    )
    db.add(db_return)
    await db.commit()
    await db.refresh(db_return)
    return db_return

async def get_return(db: AsyncSession, return_id: int):
    result = await db.execute(select(models.Return).where(models.Return.id == return_id))
    return result.scalars().first()

async def get_all_returns(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Return).offset(skip).limit(limit))
    return result.scalars().all()


async def update_return_status(db: AsyncSession, return_id: int, status: str):
    db_return = await get_return(db, return_id)
    if db_return:
        db_return.status = status
        await db.commit()
        await db.refresh(db_return)
    return db_return
