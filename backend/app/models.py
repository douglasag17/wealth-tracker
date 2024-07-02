from typing import Optional
from sqlmodel import Field, SQLModel


class Transaction(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    category: str = Field(default="")
    amount: float = Field(default=0.0)

class TransactionCreate(Transaction):
    pass