from app.models.ticket import AIResult, Ticket
from sqlalchemy.orm import Session
from random import choice

QUEUE_TO_CATEGORY = {
    "Technical Support": "technical",
    "IT Support": "technical",
    "Billing and Payments": "billing",
    "Customer Service": "general",
    "Product Support": "general"
}

PRIORITY_TO_CONFIDENCE = {
    "Critical": "high",
    "Medium": "medium",
    "Low": "low"
}


def process_ticket(db: Session, ticket: Ticket):
    text = ticket.text
    # Dummy logic (replace with ML model)
    if "invoice" in text.lower():
        category = "billing"
    elif "crash" in text.lower() or "error" in text.lower():
        category = "technical"
    else:
        category = "general"

    confidence = "medium"
    summary = ticket.subject or ticket.text[:100]

    ai_result = AIResult(
        ticket_id=ticket.id,
        category=category,
        confidence=confidence,
        summary=summary
    )
    db.add(ai_result)
    db.commit()


def mock_classify(text: str):
    keywords = {
        "billing": "billing",
        "invoice": "billing",
        "charge": "billing",
        "RAM": "technical",
        "crash": "technical",
        "analytics": "technical",
        "information": "general",
        "services": "general"
    }
    for keyword, category in keywords.items():
        if keyword in text.lower():
            return category
    return choice(["technical", "billing", "general"])


def mock_confidence(text: str):
    if "crash" in text:
        return "high"
    if "question" in text:
        return "medium"
    return "low"


def mock_summary(text: str):
    return text.split(".")[0] + "." if "." in text else text[:100]


def process_ticket_ai(text: str):
    category = mock_classify(text)
    confidence = mock_confidence(text)
    summary = mock_summary(text)
    return category, confidence, summary
