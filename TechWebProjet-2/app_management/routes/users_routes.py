from fastapi import APIRouter, HTTPException, Request, status, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from typing import Annotated

from app_management.user_login import manager
from app_management.schema.schema import UserSchema 

from app_management.services import users_services

user_router = APIRouter(prefix = "/users")
templates = Jinja2Templates(directory = "templates")

@user_router.get('/me')
def current_user_route(user: UserSchema = Depends(manager)):
    """Fonction et route pour GET l'utilisateur actuel"""
    return user


@user_router.get('/new/user')
def ask_to_add_new_user(request: Request):
    """Fonction et route pour GET la page pour crée un nouvel utilisateur"""
    return templates.TemplateResponse(
        "users/new_user_page.html",
        context={
            'request': request
        }
    )

@user_router.post('/new/user')
def create_new_user(firstname: Annotated[str, Form()], name: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()],):
    """Fonction et route pour POST le nouvel utilisateur"""
    # Vérifier si l'email existe déjà
    if users_services.get_user_by_email(email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists!"
        )

    user = {
        'firstname': firstname,
        'name': name,
        'id': 0,
        'email': email,
        'password': password,
        'role': "client"
    }

    try:
        new_user = UserSchema.model_validate(user)
        print(new_user)
    except ValidationError:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bad credentials!"
        )
    users_services.add_new_user(new_user)
    return RedirectResponse(url='/users/login', status_code=302)

@user_router.post('/change/password')
def change_password(current_password: Annotated[str, Form()], new_password: Annotated[str, Form()], user: UserSchema = Depends(manager.optional)):
    """Fonction et route pour POST changer le password de l'utilisateur actuel"""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You must be logged in to change your password!"
        )
    
    try:
        users_services.change_password(current_password, new_password, user.email)
        return RedirectResponse(url="/users/profile", status_code=302)
    except Exception as e:
        print(f"Error changing password: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Could not update password. Please check your current password and try again."
        )

@user_router.post('/change/user/information')
def change_user_information(new_firstname: Annotated[str, Form()], new_name: Annotated[str, Form()], new_email: Annotated[str, Form()], user: UserSchema = Depends(manager.optional)):
    """Fonction et route pour POST changer les informations de l'utilisateur actuel"""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You must be logged in to change your information!"
        )
    
    try:
        users_services.change_user_information(new_firstname, new_name, new_email, user.email)
        return RedirectResponse(url="/users/profile", status_code=302)
    except Exception as e:
        print(f"Error changing user information: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Could not update user information. Please try again."
        )


@user_router.get('/home')
def get_home_page(request: Request):
    """Fonction et route pour GET la page home"""
    return templates.TemplateResponse(
        "home_page.html",
        context={
            'request': request
        }
    )

@user_router.get('/login')
def get_login_page(request: Request):
    """Fonction et route pour GET la page login"""
    return templates.TemplateResponse(
        "users/login_page.html",
        context={
            'request': request
        }
    )

@user_router.post('/login')
def user_login(email: Annotated[str, Form()],password: Annotated[str, Form()]):
    """Fonction et route pour POST faire le login de l'utilisateur avec l'email et le password indiquer"""
    if users_services.get_user_by_email(email) is None or users_services.get_user_by_email(email).password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Wrong password or email!"
        ) 
    access_token = manager.create_access_token(data={'sub': email})

    response = RedirectResponse(url="/menu/all/dishes", status_code=302)
    response.set_cookie(
        key=manager.cookie_name,
        value=access_token,
        httponly=True
    )
    return response

@user_router.post('/logout')
def user_logout():
    """Fonction et route pour POST faire le logout et aller sur la page home"""
    response = RedirectResponse(url="/users/home", status_code=302)
    response.delete_cookie(
        key=manager.cookie_name,
        httponly=True
    )
    return response

@user_router.get('/profile')
def ask_to_go_to_profile(request: Request, user: UserSchema = Depends(manager.optional)):
    """Fonction et route pour GET la page profile"""
    if not user:
        return RedirectResponse(url="/users/login", status_code=302)
    return templates.TemplateResponse(
        "users/profile_page.html",
        {
            'request': request, 
            'active_user': user
        }
    )