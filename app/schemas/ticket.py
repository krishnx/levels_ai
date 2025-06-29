from pydantic import BaseModel, Field, model_validator
from typing import Optional


class TicketRequest(BaseModel):
    text: Optional[str] = Field(None, description="Full ticket text")
    subject: Optional[str] = Field(None, description="Ticket subject")
    body: Optional[str] = Field(None, description="Ticket body")

    @model_validator(mode='after')
    @classmethod
    def check_text_or_subject_body(cls, values):
        text, subject, body = values.text, values.subject, values.body
        if not text and not (subject and body):
            raise ValueError("Either 'text' or both 'subject' and 'body' must be provided")
        return values


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
