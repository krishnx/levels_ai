from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_ticket_openai(text: str) -> dict:
    prompt = f"""Classify the following customer support message into one of the following categories:
1. Technical
2. Billing
3. General

Also generate a one-sentence summary and assign a confidence level:
- "Critical" for high
- "Medium" for medium
- "Low" for low

Message:
{text}

Respond in this JSON format:
{{"category": "...", "summary": "...", "priority": "..."}}
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    import json
    try:
        ai_data = json.loads(response.choices[0].message.content)
    except Exception as e:
        raise ValueError(f"Failed to parse AI response: {e}\n\nRaw: {response.choices[0].message.content}")

    # Confidence mapping
    priority_map = {
        "Critical": "high",
        "Medium": "medium",
        "Low": "low"
    }

    return {
        "category": ai_data["category"].lower(),
        "summary": ai_data["summary"],
        "priority": ai_data["priority"],
        "confidence": priority_map.get(ai_data["priority"], "medium")  # default to medium
    }
