import random
from sqlalchemy import select
from fastapi import HTTPException, status

from app_management.db_manager import Session
from app_management.sql.sql_models import User
from app_management.schema.schema import UserSchema

def get_user_by_email(email: str):
    """Fonction pour accèder à la base de donnée et prendre l'utilisateur avec l'email passer comme paramètre"""
    with Session() as session:
        try:
            statement = select(User).filter_by(email=email)
            user = session.scalars(statement).first()
            print(f"Found user: {user.email if user else None}")
            return user
        except Exception as e:
            print(f"Error getting user: {str(e)}")
            return None

def add_new_user(user_values: UserSchema):
    """Fonction pour ajouter un utilisateur à la base de donnée"""
    with Session() as session:
        user = User(
            firstname = user_values.firstname,
            name = user_values.name,
            id = generate_id(),
            email = user_values.email,
            password = user_values.password,
            role = "client",
        )
        session.add(user)
        session.commit()
    
    return user

def generate_id():
    """Fonction pour génèrer une id unique pour les utilisateurs"""
    result = 1
    for i in range(10):
        result = result + random.randint(1,10) * result

    return result
    
def change_password(curr, new, user_email):
    """Fonction qui accède à la base de donnée et change le password de l'utilisateur avec l'email passer comme paramètre"""
    with Session() as session:
        statement = select(User).filter_by(email=user_email)
        user = session.scalars(statement).one()
        if curr == user.password:
            user.password = new
            session.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Wrong Password!",
            )

def change_user_information(new_firstname, new_name, new_email, user_email):
    """Fonction qui accède à la base de donnée et change le nom, le pénom, et l'email de l'utilisateur avec l'email passer comme paramètre"""
    with Session() as session:
        statement = select(User).filter_by(email=user_email)
        user = session.scalars(statement).one()

        user.firstname = new_firstname
        user.name = new_name
        user.email = new_email

        session.commit()