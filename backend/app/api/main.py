from app.api.routes import transactions
from fastapi import APIRouter, FastAPI
from app.db import create_db_and_tables


app = FastAPI(title="Wealth Tracker")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/health-check")
async def get_health_check():
    return {"Hello": "World!!!"}


router = APIRouter()
app.include_router(router)
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
