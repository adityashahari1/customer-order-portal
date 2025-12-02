from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .models import TicketStatus, TicketPriority

class TicketBase(BaseModel):
    subject: str
    description: str
    priority: TicketPriority = TicketPriority.MEDIUM

class TicketCreate(TicketBase):
    user_id: int

class TicketUpdate(BaseModel):
    status: Optional[TicketStatus] = None
    agent_id: Optional[int] = None
    priority: Optional[TicketPriority] = None

class Ticket(TicketBase):
    id: int
    user_id: int
    agent_id: Optional[int]
    status: TicketStatus
    created_at: datetime
    updated_at: Optional[datetime]
    sla_deadline: Optional[datetime]

    class Config:
        from_attributes = True
