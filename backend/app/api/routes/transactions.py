from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session
from app.models import Transaction


router = APIRouter()


@router.post("/")
async def add_transaction(
    transaction: Transaction, session: AsyncSession = Depends(get_session)
):
    session.add(transaction)
    await session.commit()
    await session.refresh(transaction)
    return transaction


@router.get("/", response_model=list[Transaction])
async def get_transactions(session: AsyncSession = Depends(get_session)):
    transactions = await session.execute(select(Transaction)).all()
    return transactions
