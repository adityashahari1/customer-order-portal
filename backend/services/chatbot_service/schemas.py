from pydantic import BaseModel

class ChatMessage(BaseModel):
    message: str
    user_email: str

class ChatResponse(BaseModel):
    response: str
