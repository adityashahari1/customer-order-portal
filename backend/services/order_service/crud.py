from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from . import models, schemas

async def get_order(db: AsyncSession, order_id: int):
    result = await db.execute(
        select(models.Order)
        .options(selectinload(models.Order.items))
        .where(models.Order.id == order_id)
    )
    return result.scalars().first()

async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.Order)
        .options(selectinload(models.Order.items))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def create_order(db: AsyncSession, order: schemas.OrderCreate):
    db_order = models.Order(
        user_id=order.user_id,
        total_amount=order.total_amount,
        status=models.OrderStatus.PENDING.value
    )
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)

    for item in order.items:
        db_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(db_item)
    
    await db.commit()
    
    # Record history
    history = models.OrderStateHistory(
        order_id=db_order.id,
        from_status=None,
        to_status=models.OrderStatus.PENDING.value
    )
    db.add(history)
    await db.commit()
    
    # Eagerly load items relationship to prevent async serialization errors
    result = await db.execute(
        select(models.Order)
        .options(selectinload(models.Order.items))
        .where(models.Order.id == db_order.id)
    )
    return result.scalars().first()

async def update_order_status(db: AsyncSession, order_id: int, status: str):
    db_order = await get_order(db, order_id)
    if db_order:
        old_status = db_order.status
        db_order.status = status
        
        history = models.OrderStateHistory(
            order_id=db_order.id,
            from_status=old_status,
            to_status=status
        )
        db.add(history)
        await db.commit()
        await db.refresh(db_order)
    return db_order
