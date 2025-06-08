from sqlalchemy import select, or_
from fastapi import HTTPException, status


from app_management.db_manager import Session
from app_management.sql.sql_models import Table

def book_table(people_count, day, time, user):
    """
    Fonction pour réserver une table, elle controle si une table est disponible pour le nombre de personnes,
    passer comme paramètre.
    """
    with Session() as session:
        statement = select(Table).where(
            Table.available == True,
            or_(
                Table.tablecapacity == people_count, 
                Table.tablecapacity > people_count
                ),
        ).order_by(Table.tablecapacity).limit(1)
        table = session.scalars(statement).one()

        try:
            table.clientid = user.id
            table.available = False
            table.day = day
            table.time = time
        except Exception as er:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="You must be logged in to book a table!",
            )

        session.commit()

def get_tables():
    """Fonction pour accèder à toutes les tables dans la base de donnée"""
    with Session() as session:
        statement = select(Table)
        tables = session.scalars(statement).all()
    return tables

def change_availability(table_id):
    """
    Fonction pour changer la disponibilité de la table avec l'id == table_id.
    La fonction change le paramètre available à True et mets le jour et heure à vide et le clientid à 0
    """
    with Session() as session:
        statement = select(Table).filter_by(tableid=table_id)
        table = session.scalars(statement).one()
        
        if not table.available:
            table.clientid = 0
            table.day = ''
            table.time = ''
            table.available = True
            
        session.commit()