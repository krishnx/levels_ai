from fastapi import FastAPI
from app.api.routes import router as api_router
from dotenv import load_dotenv

app = FastAPI(title="Customer Support Intelligence API")
app.include_router(api_router)

load_dotenv()

@app.get("/")
def read_root():
    return {"message": "Customer Support Intelligence API is running"}