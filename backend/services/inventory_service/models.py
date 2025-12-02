from sqlalchemy import Column, Integer, String, Float
from backend.shared.database import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    sku = Column(String, unique=True, index=True)
    stock = Column(Integer, default=0)
    price = Column(Float, default=0.0)
    category = Column(String, nullable=True)
    warehouse_location = Column(String, nullable=True)
    reorder_threshold = Column(Integer, default=10)
