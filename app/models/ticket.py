from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base
from pydantic import BaseModel, Field
from typing import Optional


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    text = Column(Text, nullable=False)
    language = Column(String, default="EN")
    created_at = Column(DateTime, default=datetime.utcnow)

    ai_result = relationship("AIResult", uselist=False, back_populates="ticket")


class AIResult(Base):
    __tablename__ = "ai_results"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    category = Column(String)
    confidence = Column(String)
    summary = Column(Text)

    ticket = relationship("Ticket", back_populates="ai_result")


class TicketRequest(BaseModel):
    # Accept either 'text' alone or 'subject' and 'body' optionally
    text: Optional[str] = Field(None, description="Full ticket text")
    subject: Optional[str] = Field(None, description="Ticket subject")
    body: Optional[str] = Field(None, description="Ticket body")

    model_config = {
        "from_attributes": True
    }

    # Custom validation to ensure either text or (subject + body) present
    def validate(self, *args, **kwargs):
        if not self.text and not (self.subject and self.body):
            raise ValueError("Either 'text' or both 'subject' and 'body' must be provided")


class AIResultResponse(BaseModel):
    category: Optional[str]
    confidence: Optional[str]
    summary: Optional[str]

    model_config = {
        "from_attributes": True
    }


class TicketResponse(BaseModel):
    id: int
    subject: Optional[str]
    body: Optional[str]
    text: str
    language: Optional[str]
    ai_result: Optional[AIResultResponse]

    model_config = {
        "from_attributes": True
    }
