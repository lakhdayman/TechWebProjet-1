from fastapi_login import LoginManager

from app_management.services.users_services import get_user_by_email

SECRET = "SECRET"
manager = LoginManager(SECRET, '/login', use_cookie=True)
manager.cookie_name = "auth_cookie"

@manager.user_loader()
def query_user(email: str):
    return get_user_by_email(email)