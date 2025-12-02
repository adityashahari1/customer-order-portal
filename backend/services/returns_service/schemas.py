from pydantic import BaseModel
from .models import ReturnStatus

class ReturnBase(BaseModel):
    order_id: int
    reason: str
    refund_amount: float

class ReturnCreate(ReturnBase):
    pass

class ReturnUpdate(BaseModel):
    status: ReturnStatus

class Return(ReturnBase):
    id: int
    status: ReturnStatus

    class Config:
        from_attributes = True
