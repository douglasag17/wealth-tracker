from typing import List

from fastapi import APIRouter
from sqlmodel import select, Session

from app.db import engine
from app.models import Transaction


router = APIRouter()

@router.post("/")
def add_transaction(transaction: Transaction):
    with Session(engine) as session:
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction


@router.get("/")
def get_transactions():
    with Session(engine) as session:
        transactions = session.exec(select(Transaction)).all()
        return transactions