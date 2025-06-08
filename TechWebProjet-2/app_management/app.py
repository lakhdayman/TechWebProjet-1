from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app_management.routes.users_routes import user_router
from app_management.routes.menu_routes import menu_router
from app_management.routes.orders_routes import order_router
from app_management.routes.table_booking_routes import table_router
from app_management.routes.feedback_routes import feedback_router

from app_management.db_manager import create_database

#Définir ou se trouve les templates HTML
templates = Jinja2Templates(directory = "templates")

app = FastAPI(title = "Burger King")
#Définir ou se trouve les fichier statics comme .css .js ou des images
app.mount("/static", StaticFiles(directory = "static"))
app.mount("/images", StaticFiles(directory = "images"))

#Inclusion des routers dans l'application
app.include_router(user_router)
app.include_router(menu_router)
app.include_router(order_router)
app.include_router(table_router)
app.include_router(feedback_router)

@app.get("/")
def root():
    """Redirection de la page d'accueil vers /users/home"""
    return RedirectResponse(url="/users/home", status_code=302)

@app.on_event('startup')
def on_startup():
    """Creation de la base de donnée en lancant le serveur et print un petit message dans la console"""
    print("'Burger King' is on AIR!")
    create_database()

@app.on_event('shutdown')
def on_shutdown():
    """Print un petit message dans la console"""
    print("'Burger King' is down!")

@app.exception_handler(422)
def error_422_redirection(request: Request, exception: HTTPException):
    """Fonction executé lors d'une erreur 422 -> l'utilisateur est dirigé vers la page 422.html"""
    return templates.TemplateResponse("errors/422.html", {"request": request, "exception": exception}, status_code=422)

@app.exception_handler(404)
def error_404_redirection(request: Request, exception: HTTPException):
    """Fonction executé lors d'une erreur 404 -> l'utilisateur est dirigé vers la page 404.html"""
    return templates.TemplateResponse("errors/404.html", {"request": request, "exception": exception}, status_code=404)

@app.exception_handler(400)
def error_400_redirection(request: Request, exception: HTTPException):
    """Fonction executé lors d'une erreur 424002 -> l'utilisateur est dirigé vers la page 400.html"""
    return templates.TemplateResponse("errors/400.html", {"request": request, "exception": exception}, status_code=400)

@app.exception_handler(401)
def error_401_redirection(request: Request, exception: HTTPException):
    """Fonction executé lors d'une erreur 401 -> l'utilisateur est dirigé vers la page 401.html"""
    return templates.TemplateResponse("errors/401.html", {"request": request, "exception": exception}, status_code=401)

