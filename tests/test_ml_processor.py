from app.models.ticket import Ticket
from app.services.ml_processor import process_ticket
from app.db.session import SessionLocal

def test_ml_classification():
    db = SessionLocal()
    ticket = Ticket(text="I have an error with the analytics dashboard")
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    process_ticket(db, ticket)
    assert ticket.ai_result.category == "technical"
    db.close()
