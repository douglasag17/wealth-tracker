from typing import Union, List

from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


from app.db import get_session
from app.models import Transaction, TransactionCreate


router = APIRouter()


@router.get("/", response_model=List[Transaction])
async def get_transactions(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Transaction))
    transactions = result.scalars().all()
    return [Transaction(id=transaction.id, category=transaction.category, amount=transaction.amount) for transaction in transactions]


@router.post("/")
async def add_transaction(transaction: TransactionCreate, session: AsyncSession = Depends(get_session)):
    new_transaction = Transaction(category=transaction.category, amount=transaction.amount)
    session.add(new_transaction)
    await session.commit()
    await session.refresh(new_transaction)
    return new_transaction


@router.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
