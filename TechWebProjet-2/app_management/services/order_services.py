from sqlalchemy import select
from fastapi import HTTPException, status

from app_management.db_manager import Session
from app_management.sql.sql_models import Dish, Order
from app_management.schema.schema import DishSchema, OrderSchema

def get_orders():
    """Fonction pour accèder aux commandes dans la base de donnée"""
    with Session() as session:
        statement = select(Order)
        orders = session.scalars(statement).all()

    return orders

def add_to_basket(dish_id, user):
    """Fonction pour ajouter un plats à la commande de l'utilisateur"""
    with Session() as session:
        statement = select(Dish).filter_by(dishid= dish_id)
        dish = session.scalars(statement).one()

        statement = select(Order)
        orders = session.scalars(statement).all()
        try:
            statement = select(Order).where(Order.clientid == user.id, Order.complete == False)
        except Exception as er:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="You must be logged in to order!",
            )
        try:
            current_order = session.scalars(statement).one()
            current_order.dishes = current_order.dishes + "," + dish.dishname
            current_order.orderprice = current_order.orderprice + dish.price
        except:
            order = Order(
                orderid= len(orders) + 1,
                clientid= user.id,
                dishes= dish.dishname,
                orderprice= dish.price,
                complete= False, 
                status="working"
            )

            session.add(order)

        session.commit()

def cancel_order(user):
    """Fonction pour annuler une commande -> supprimer la commande de la base de donnée"""
    with Session() as session:
        try:
            statement = select(Order).where(Order.clientid == user.id, Order.complete == False)
            order = session.scalars(statement).one()

            session.delete(order)
            session.commit()
        except Exception as er:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="You must be logged in to cancel!",
            )
        
def checkout(user):
    """Fonction pour finaliser la commande -> mettre le paramètre complete comme True"""
    with Session() as session:
        try:
            statement = select(Order).where(Order.clientid == user.id, Order.complete == False)
            order = session.scalars(statement).one()
            order.complete = True
            session.commit()
        except Exception as er:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="You must be logged in to checkout!",
            )

def remove_from_basket(dish_id, user):
    """Fonction pour enlèver un plat de la commande"""
    with Session() as session:
        try:
            statement = select(Order).where(Order.clientid == user.id, Order.complete == False)
            order = session.scalars(statement).one()

            statement = select(Dish).filter_by(dishid=dish_id)
            dish_to_remove = session.scalars(statement).one()

            order.dishes = order.dishes.replace(dish_to_remove.dishname, "", 1)
            order.orderprice = order.orderprice - dish_to_remove.price
            session.commit()
        except Exception as er:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="You must be logged in to order!",
            )

def mark_as_complete(order_id):
    """Fonction pour indiquer que la commande est prête"""
    with Session() as session:
        statement = select(Order).filter_by(orderid= order_id)
        order = session.scalars(statement).one()

        order.status = "ready"
        session.commit()