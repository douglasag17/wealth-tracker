from app.api.routes import transactions
from fastapi import APIRouter, FastAPI
from app.db import init_db


app = FastAPI(title="Wealth Tracker")


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/health-check")
async def get_health_check():
    return {"Hello": "World!!!"}


router = APIRouter()
app.include_router(router)
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
