from pydantic import BaseModel
from typing import List, Dict

class DashboardMetrics(BaseModel):
    total_orders: int
    total_revenue: float
    pending_orders: int
    active_tickets: int
    inventory_alerts: int

class SalesData(BaseModel):
    date: str
    amount: float
