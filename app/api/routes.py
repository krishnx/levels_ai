from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.ticket import TicketRequest, TicketResponse
from app.db.session import get_db
from app.models.ticket import Ticket
from app.services.ml_processor import process_ticket

router = APIRouter()

@router.post("/requests", response_model=TicketResponse)
def create_ticket(payload: TicketRequest, db: Session = Depends(get_db)):
    # Prepare text if not given
    text = payload.text
    if not text:
        text = f"{payload.subject} {payload.body}".strip()

    ticket = Ticket(subject=payload.subject, body=payload.body, text=text)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    process_ticket(db, ticket)
    return ticket

@router.get("/requests/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.get("/requests", response_model=List[TicketResponse])
def filter_tickets(category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Ticket)
    if category:
        query = query.filter(Ticket.ai_result.has(category=category))
    return query.all()
