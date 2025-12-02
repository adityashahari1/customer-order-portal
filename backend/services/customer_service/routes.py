from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from backend.shared.database import get_db
from backend.shared import auth
from . import crud, schemas, models

router = APIRouter()

@router.post("/", response_model=schemas.Ticket)
async def create_ticket(
    ticket: schemas.TicketCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    return await crud.create_ticket(db=db, ticket=ticket)

@router.get("/", response_model=List[schemas.Ticket])
async def read_tickets(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    return await crud.get_tickets(db, skip=skip, limit=limit)

@router.get("/{ticket_id}", response_model=schemas.Ticket)
async def read_ticket(
    ticket_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    db_ticket = await crud.get_ticket(db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket

@router.put("/{ticket_id}", response_model=schemas.Ticket)
async def update_ticket(
    ticket_id: int, 
    updates: schemas.TicketUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user)
):
    db_ticket = await crud.update_ticket(db, ticket_id=ticket_id, updates=updates)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket
