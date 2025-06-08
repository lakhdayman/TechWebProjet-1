from fastapi import APIRouter, HTTPException, Request, status, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from typing import Annotated

from app_management.user_login import manager
from app_management.schema.schema import FeedbackSchema
from app_management.services import feedback_services, users_services

feedback_router = APIRouter(prefix="/feedbacks")
templates = Jinja2Templates(directory="templates")

@feedback_router.post('/feedback')
def leave_feedback(email: Annotated[str, Form()], password: Annotated[str, Form()], users_feedback: Annotated[str, Form()]):
    """Fonction et route POST pour laisser un feedback -> ajouter un feedback à la base de donnée"""
    if users_services.get_user_by_email(email).password == password:
        feedback_services.leave_feedback(users_feedback, email)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Wrong password or email!"
        )
    return RedirectResponse(url="/users/home", status_code=302)