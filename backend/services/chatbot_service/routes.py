from fastapi import APIRouter, Depends
from typing import Optional
from backend.shared import auth
from . import schemas, chat_manager

router = APIRouter()

async def get_optional_user(token: Optional[str] = None) -> Optional[dict]:
    """Get current user if token provided, otherwise allow guest access"""
    if token:
        try:
            return await auth.get_current_user(token)
        except:
            return None
    return None

@router.post("/chat", response_model=schemas.ChatResponse)
async def chat(
    message: schemas.ChatMessage, 
    current_user: Optional[dict] = Depends(get_optional_user)
):
    user_email = message.user_email
    if current_user:
        user_email = current_user.get('username', message.user_email)
    
    response = await chat_manager.process_message(message.message, user_email)
    return {"response": response}

