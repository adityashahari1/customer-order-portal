from pydantic import BaseModel, EmailStr

class EmailRequest(BaseModel):
    to_email: EmailStr
    subject: str
    content: str

class SMSRequest(BaseModel):
    to_number: str
    body: str
