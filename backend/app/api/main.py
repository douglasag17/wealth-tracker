from app.api.routes import transactions
from fastapi import APIRouter, FastAPI

app = FastAPI(title="Wealth Tracker")
router = APIRouter()
app.include_router(router)
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
