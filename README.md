# Customer Support Intelligence API

## Overview

This FastAPI backend processes customer support requests, classifies them into technical, billing, or general categories using AI, and stores results in a PostgreSQL database. The system includes:

- REST API endpoints to create and retrieve support requests.
- AI-powered classification and summary generation.
- PostgreSQL with SQLAlchemy ORM and Alembic migrations.
- Dockerized environment for easy setup.

---

## API Endpoints
- POST /requests — Create a support request 
- GET /requests/{id} — Get support request by ID 
- GET /requests?category=technical — List requests filtered by category 
- GET /stats — Get counts per category in the last 7 days

## Setup Instructions

### Prerequisites

- Docker & Docker Compose installed on your system
```commandline
# 1. Build and start containers:
docker-compose up --build -d

# 2. Apply database migrations:
docker-compose exec web alembic upgrade head

# 3. Restart the web service to ensure fresh state:
docker-compose restart web

# 4. Run pytests
docker-compose exec web pytest

# 5. check logs
docker-compose logs web
```
- Python 3.11+ (optional if running outside Docker)
- `psql` CLI (optional for database inspection)
- Access API docs at http://localhost:8000/docs

---

### Environment Variables

Create a `.env` file in the project root:

```env
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=support_tickets
DATABASE_URL=postgresql+psycopg2://myuser:mypassword@db:5432/support_tickets
OPENAI_API_KEY=your_openai_api_key_here
