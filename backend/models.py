from typing import List, Optional
from sqlmodel import SQLModel, Field


class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)


class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    account_id: int = Field(default=None, foreign_key="account.id")
    amount: float = Field(default=0.0, nullable=False)
    description: str = Field(nullable=False)
