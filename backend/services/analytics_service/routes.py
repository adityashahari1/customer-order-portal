from fastapi import APIRouter, Depends
from typing import List
from backend.shared import auth
from . import schemas
import random
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/dashboard", response_model=schemas.DashboardMetrics)
async def get_dashboard_metrics(
    current_user: dict = Depends(auth.get_current_user)
):
    # Mock data for demonstration
    return {
        "total_orders": 1250,
        "total_revenue": 150000.00,
        "pending_orders": 45,
        "active_tickets": 12,
        "inventory_alerts": 3
    }

@router.get("/sales", response_model=List[schemas.SalesData])
async def get_sales_data(
    days: int = 7,
    current_user: dict = Depends(auth.get_current_user)
):
    # Mock data
    data = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        data.append({
            "date": date,
            "amount": random.uniform(1000, 5000)
        })
    return data
