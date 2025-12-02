from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
import enum
from backend.shared.database import Base

class TicketStatus(str, enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class TicketPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"

class CustomerTicket(Base):
    __tablename__ = "customer_tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    agent_id = Column(Integer, nullable=True)
    subject = Column(String)
    description = Column(String)
    status = Column(String, default=TicketStatus.OPEN.value)
    priority = Column(String, default=TicketPriority.MEDIUM.value)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    sla_deadline = Column(DateTime(timezone=True))
