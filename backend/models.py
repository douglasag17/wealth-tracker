from typing import List, Optional
from sqlmodel import SQLModel, Field
from decimal import Decimal


class Currency(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)  # COP, USD


class AccountType(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    type: str = Field(nullable=False)


class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    account_type_id: int = Field(default=None, foreign_key="accounttype.id")
    currency_id: int = Field(default=None, foreign_key="currency.id")


class Category(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)


class SubCategory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    category_id: int = Field(default=None, foreign_key="category.id")
    type: str = Field(nullable=False)  # must, need, want


class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    account_id: int = Field(default=None, foreign_key="account.id")
    transaction_type: str = Field(nullable=False, default="income")  # income, expense
    subcategory_id: int = Field(default=None, foreign_key="subcategory.id")
    amount: Decimal = Field(default=0, max_digits=50, decimal_places=2, nullable=False)
    description: str = Field(nullable=False)
    # created_at: str = Field(default=None)  # TODO:
    # is_paid: bool  # TODO:
    # is_planned: bool  # TODO:


class MonthlyBudget(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    subcategory_id: int = Field(default=None, foreign_key="subcategory.id")
    year: int  # TODO:
    month: int  # TODO:
    budgeted: Decimal  # TODO:
