from datasets import load_dataset
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.ticket import Ticket, AIResult
from app.services.ml_processor import process_ticket

Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    dataset = load_dataset("tobi-bueck/customer-support-tickets", split="train")

    for row in dataset:
        if row['language'] != 'EN':
            continue

        text = f"{row.get('subject', '')} {row.get('body', '')}".strip()
        ticket = Ticket(
            subject=row.get('subject'),
            body=row.get('body'),
            text=text,
            language=row.get('language', 'EN')
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        process_ticket(db, ticket)

    db.close()

if __name__ == "__main__":
    seed()