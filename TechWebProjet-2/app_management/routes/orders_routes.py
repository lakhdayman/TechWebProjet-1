from fastapi import APIRouter, HTTPException, Request, status, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from typing import Annotated
from app_management.user_login import manager
from app_management.schema.schema import OrderSchema, UserSchema
from app_management.services import order_services, menu_services

order_router = APIRouter(prefix="/orders")
templates = Jinja2Templates(directory="templates")

@order_router.get('/order')
def ask_to_order(request: Request, user: UserSchema = Depends(manager.optional)):
    """Fonction et route GET pour aller sur la page des commandes"""
    if not user:
        return RedirectResponse(url="/users/login", status_code=302)
    menu = menu_services.get_menu()
    return templates.TemplateResponse(
        "/orders/order_page.html",
        context={'request': request, 'menu': menu, 'active_user': user}
    )

@order_router.get('/my/orders')
def ask_to_get_my_order(request: Request, user: UserSchema = Depends(manager.optional)):
    """Fonction et route GET pour aller sur la page des commandes de l'utilisteur actuel"""
    orders = order_services.get_orders()
    return templates.TemplateResponse(
        "/users/my_orders.html",
        context={'request': request, 'user': user, 'orders': orders}
    )

@order_router.post('/add/basket')
def add_dish_to_basket(dishid: Annotated[str, Form()], user: UserSchema = Depends(manager.optional)):
    """Fonction et route POST pour ajouter un plat à la commande de l'utilisateur actuel"""
    order_services.add_to_basket(dishid, user)
    return RedirectResponse(url="/orders/order", status_code=302)


@order_router.post('/remove/basket')
def remove_dish_from_basket(dishid: Annotated[str, Form()], user: UserSchema = Depends(manager.optional)):
    """Fonction et route POST pour supprimer un plat de la commande de l'utilisateur actuel"""
    order_services.remove_from_basket(dishid, user)
    return RedirectResponse(url="/orders/order", status_code=302)

@order_router.post('/checkout')
def checkout(user: UserSchema = Depends(manager.optional)):
    """Fonction et route POST pour faire le checkout de la commande"""
    order_services.checkout(user)
    return RedirectResponse(url="/menu/all/dishes",status_code=302)

@order_router.post('/cancel/order')
def cancel_order(user: UserSchema = Depends(manager.optional)):
    """Fonction et route POST pour annuler la commande de l'utilisateur actuel"""
    order_services.cancel_order(user)
    return RedirectResponse(url="/menu/all/dishes",status_code=302)

@order_router.get('/get/orders')
def ask_to_manage_orders(request: Request):
    """Fonction et route GET pour acceder à la page pour gérer les commandes"""
    orders = order_services.get_orders()
    return templates.TemplateResponse(
        "/orders/orders_managment.html",
        context={'request': request, 'orders': orders}
    )

@order_router.post('/complete')
def mark_order_as_completed(orderid: Annotated[str, Form()]):
    """Fonction et route POST pour marquer la commander avec l'id passer comme paramètre, comme complete"""
    order_services.mark_as_complete(orderid)
    return RedirectResponse(url="/orders/get/orders",status_code=302)
