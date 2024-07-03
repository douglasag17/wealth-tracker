from fastapi import FastAPI
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from .database import create_db_and_tables, engine
from .models import Transaction


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    The first part of the function, before the yield, will be executed before the application starts.
    And the part after the yield will be executed after the application has finished.

    Args:
        app (FastAPI): FastAPI App
    """
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/transactions/", response_model=Transaction)
def create_hero(transaction: Transaction):
    with Session(engine) as session:
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction


@app.get("/transactions/", response_model=list[Transaction])
def read_heroes():
    with Session(engine) as session:
        transactions = session.exec(select(Transaction)).all()
        return transactions
