from sqlalchemy import select
from fastapi import HTTPException, status

from app_management.db_manager import Session
from app_management.sql.sql_models import Dish
from app_management.schema.schema import DishSchema
from app_management.services import users_services

def get_menu():
    """Fonction pour accèder aux plats dans la base de donnée"""
    with Session() as session: 
        statement = select(Dish)
        menu = session.scalars(statement).all()
    return [Dish(
        dishid = dish.dishid,
        dishname = dish.dishname,
        dishtype = dish.dishtype,
        price = dish.price 
    )
    for dish in menu
    ]

def add_dish(new: DishSchema):
    """Fonction pour ajouter un plat à la base de donnée"""
    with Session() as session:
        statement = select(Dish)
        menu = session.scalars(statement).all()
        dish = Dish(
            dishid = users_services.generate_id(),
            dishname = new.dishname,
            dishtype = new.dishtype,
            price = new.price
            )
        session.add(dish)
        session.commit()
    return dish

def remove_dish_by_id(id_to_delete):
    """Fonction pour supprimer un plat de la base de donnée"""
    with Session() as session:
        try:
            statement = select(Dish).filter_by(dishid= id_to_delete)
            dish = session.scalars(statement).one()
            session.delete(dish)
            session.commit()
        except Exception as er:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No dish was found with that id!",
            )

def edit_dish_by_id(id_to_edit, updated_dish):
    """
    Fonction pour editer un plat de la base de donnée avec l'id == id_to_edit
    Elle change le nom, le type et le prix
    """
    with Session() as session:
        try:
            statement = select(Dish).filter_by(dishid= id_to_edit)
            dish = session.scalars(statement).one()

            dish.dishname = updated_dish.dishname
            dish.dishtype = updated_dish.dishtype
            dish.price = updated_dish.price

            session.commit()
        except Exception as er:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No dish was found with that id!",
            )