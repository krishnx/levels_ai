- REST API: create, retrieve, filter support tickets
- AI integration for classification and summary
- PostgreSQL + Alembic migrations
- Hugging Face dataset seeding

## Run Locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Seed Database
```bash
python scripts/seed_db.py
```
