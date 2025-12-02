from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
import enum
from backend.shared.database import Base

class ReturnStatus(str, enum.Enum):
    REQUESTED = "REQUESTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    RECEIVED = "RECEIVED"
    REFUNDED = "REFUNDED"

class Return(Base):
    __tablename__ = "returns"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, index=True)
    reason = Column(String)
    status = Column(String, default=ReturnStatus.REQUESTED.value)
    refund_amount = Column(Float)
