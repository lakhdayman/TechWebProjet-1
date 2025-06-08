from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app_management.schema.schema import UserSchema
from app_management.services import table_booking_services
from app_management.user_login import manager

table_router = APIRouter(prefix="/table")
templates = Jinja2Templates(directory="templates")

@table_router.get('/book/table')
def ask_to_book_a_table(request: Request):
    """Fonction et route pour GET la page des tables"""
    return templates.TemplateResponse(
        "tables/book_table.html",
        context={'request': request}
    )

@table_router.post('/book/table')
def book_table(day: Annotated[str, Form()], time: Annotated[str, Form()], people_count: Annotated[str, Form()], user: UserSchema = Depends(manager.optional)):
    """Fonction et route pour POST réserver une table pour l'utilisateur actuel avec les valeurs passer comme paramètre"""
    table_booking_services.book_table(people_count, day, time, user)
    return RedirectResponse(url="/users/home", status_code=302)

@table_router.get('/manage')
def ask_to_manage_tables(request: Request):
    """Fonction et route pour GET la page manage, pour gérer les tables"""
    tables = table_booking_services.get_tables()
    return templates.TemplateResponse(
        "tables/tables.html",
        context={'request': request, 'tables': tables}
    )

@table_router.post('/change/availability')
def change_availability(tableid: Annotated[str, Form()]):
    """Fonction et route pour POST changer l'availability de la table avec l'id passer comme paramètre"""
    table_booking_services.change_availability(tableid)
    return RedirectResponse(url="/table/manage", status_code=302)