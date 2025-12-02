from fastapi import APIRouter, BackgroundTasks, Depends
from backend.shared import auth
from . import schemas, email_sender, sms_sender

router = APIRouter()

@router.post("/email")
async def send_email_notification(
    request: schemas.EmailRequest, 
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(auth.get_current_user)
):
    background_tasks.add_task(email_sender.send_email, request.to_email, request.subject, request.content)
    return {"message": "Email queued for sending"}

@router.post("/sms")
async def send_sms_notification(
    request: schemas.SMSRequest, 
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(auth.get_current_user)
):
    background_tasks.add_task(sms_sender.send_sms, request.to_number, request.body)
    return {"message": "SMS queued for sending"}
