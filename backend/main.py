from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from .database import engine, create_db_and_tables, drop_db_and_tables
from .models import Transaction, Account


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
    drop_db_and_tables()


app = FastAPI(lifespan=lifespan)


@app.post("/accounts/", response_model=Account)
def create_account(account: Account):
    with Session(engine) as session:
        session.add(account)
        session.commit()
        session.refresh(account)
        return account


@app.get("/accounts/", response_model=list[Account])
def get_accounts():
    with Session(engine) as session:
        accounts = session.exec(select(Account)).all()
        return accounts


@app.get("/accounts/{account_id}", response_model=Account)
def get_account(account_id: int):
    with Session(engine) as session:
        account = session.get(Account, account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Hero not found")
        return account


@app.post("/transactions/", response_model=Transaction)
def create_transaction(transaction: Transaction):
    with Session(engine) as session:
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction


@app.get("/transactions/", response_model=list[Transaction])
def get_transactions():
    with Session(engine) as session:
        transactions = session.exec(select(Transaction)).all()
        return transactions
