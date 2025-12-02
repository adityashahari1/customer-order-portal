from pydantic import BaseModel
from typing import Optional

class InventoryBase(BaseModel):
    name: str
    sku: str
    stock: int
    price: float
    category: Optional[str] = None
    warehouse_location: Optional[str] = None
    reorder_threshold: int = 10

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: int

class Inventory(InventoryBase):
    id: int

    class Config:
        from_attributes = True
