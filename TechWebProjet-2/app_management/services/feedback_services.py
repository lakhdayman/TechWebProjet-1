from sqlalchemy import select

from app_management.db_manager import Session
from app_management.sql.sql_models import Feedback
from app_management.schema.schema import FeedbackSchema

def leave_feedback(feedback_content, email):
    """Fonction pour ajouter un feedback à la base de donnée"""
    with Session() as session: 
        statement = select(Feedback)
        feedbacks = session.scalars(statement).all()

        feedback = Feedback(
            feedbackid= len(feedbacks) + 1,
            clientemail= email,
            feedback= feedback_content
        )
        session.add(feedback)
        session.commit()