from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.ai_model.classify_ticket_openai import classify_ticket_openai
from app.schemas.ticket import TicketRequest, TicketResponse
from app.db.session import get_db
from app.models.ticket import Ticket
from app.services.ml_processor import process_ticket

from sqlalchemy import func

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

    try:
        ai_result = classify_ticket_openai(text)
        ticket.category = ai_result["category"]
        ticket.summary = ai_result["summary"]
        ticket.confidence = ai_result["confidence"]
        ticket.priority = ai_result["priority"]

        db.commit()
        db.refresh(ticket)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI classification failed: {str(e)}")

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

@router.get("/stats", summary="Get ticket counts per category in the last 7 days")
def get_stats(db: Session = Depends(get_db)):
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    results = (
        db.query(Ticket.category, func.count(Ticket.id))
        .filter(Ticket.created_at >= seven_days_ago)
        .group_by(Ticket.category)
        .all()
    )

    # Convert to dict with 0 defaults
    stats = {"technical": 0, "billing": 0, "general": 0}
    for category, count in results:
        if category in stats:
            stats[category] = count

    return stats