from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta
from . import models, schemas

async def create_ticket(db: AsyncSession, ticket: schemas.TicketCreate):
    # Set SLA deadline based on priority (example logic)
    sla_hours = {
        models.TicketPriority.LOW: 48,
        models.TicketPriority.MEDIUM: 24,
        models.TicketPriority.HIGH: 4,
        models.TicketPriority.URGENT: 1
    }
    deadline = datetime.utcnow() + timedelta(hours=sla_hours.get(ticket.priority, 24))
    
    db_ticket = models.CustomerTicket(
        user_id=ticket.user_id,
        subject=ticket.subject,
        description=ticket.description,
        priority=ticket.priority.value,
        sla_deadline=deadline
    )
    db.add(db_ticket)
    await db.commit()
    await db.refresh(db_ticket)
    return db_ticket

async def get_ticket(db: AsyncSession, ticket_id: int):
    result = await db.execute(select(models.CustomerTicket).where(models.CustomerTicket.id == ticket_id))
    return result.scalars().first()

async def get_tickets(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.CustomerTicket).offset(skip).limit(limit))
    return result.scalars().all()

async def update_ticket(db: AsyncSession, ticket_id: int, updates: schemas.TicketUpdate):
    db_ticket = await get_ticket(db, ticket_id)
    if db_ticket:
        if updates.status:
            db_ticket.status = updates.status.value
        if updates.agent_id:
            db_ticket.agent_id = updates.agent_id
        if updates.priority:
            db_ticket.priority = updates.priority.value
        
        await db.commit()
        await db.refresh(db_ticket)
    return db_ticket
