from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict
from backend.shared.database import get_db
from backend.shared import auth

from . import crud, schemas, models

# Simple connection manager for order status updates via WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, order_id: int):
        await websocket.accept()
        if order_id not in self.active_connections:
            self.active_connections[order_id] = []
        self.active_connections[order_id].append(websocket)

    def disconnect(self, websocket: WebSocket, order_id: int):
        if order_id in self.active_connections:
            self.active_connections[order_id].remove(websocket)
            if not self.active_connections[order_id]:
                del self.active_connections[order_id]

    async def broadcast(self, message: str, order_id: int):
        if order_id in self.active_connections:
            for connection in self.active_connections[order_id]:
                await connection.send_text(message)

manager = ConnectionManager()
router = APIRouter()

# CREATE (no auth required for chatbot integration)
@router.post("/", response_model=schemas.Order)
async def create_order(
    order: schemas.OrderCreate,
    db: AsyncSession = Depends(get_db),
):
    return await crud.create_order(db=db, order=order)

# READ (unauthenticated)
@router.get("/", response_model=List[schemas.Order])
async def read_orders(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    return await crud.get_orders(db, skip=skip, limit=limit)

@router.get("/{order_id}", response_model=schemas.Order)
async def read_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
):
    db_order = await crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

# UPDATE
@router.put("/{order_id}/status", response_model=schemas.Order)
async def update_order_status(
    order_id: int,
    status_update: schemas.OrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(auth.get_current_user),
):
    db_order = await crud.update_order_status(db, order_id=order_id, status=status_update.status.value)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    await manager.broadcast(f"Order status updated to {status_update.status.value}", order_id)
    return db_order

# WEBSOCKET
@router.websocket("/ws/{order_id}")
async def websocket_endpoint(websocket: WebSocket, order_id: int):
    await manager.connect(websocket, order_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, order_id)
