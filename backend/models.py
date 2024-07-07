from typing import List
from sqlmodel import SQLModel, Field, Relationship
from decimal import Decimal
from datetime import datetime


class CurrencyBase(SQLModel):
    name: str = Field(nullable=False)  # COP, USD


class Currency(CurrencyBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    accounts: List["Account"] = Relationship(back_populates="currency")


class CurrencyPublic(CurrencyBase):
    id: int


class AccountTypeBase(SQLModel):
    type: str = Field(nullable=False)


class AccountType(AccountTypeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    accounts: List["Account"] = Relationship(back_populates="account_type")


class AccountTypePublic(AccountTypeBase):
    id: int


class AccountBase(SQLModel):
    name: str = Field(nullable=False)
    created_at: datetime | None = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
    )

    currency_id: int = Field(default=None, foreign_key="currency.id")

    account_type_id: int = Field(default=None, foreign_key="accounttype.id")


class Account(AccountBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    currency: Currency | None = Relationship(back_populates="accounts")
    account_type: AccountType | None = Relationship(back_populates="accounts")


class AccountPublic(AccountBase):
    id: int


class AccountCreate(AccountBase):
    pass


class AccountUpdate(SQLModel):
    name: str | None = None
    currency_id: int | None = None
    account_type_id: int | None = None


class AccountPublicWithTypeAndCurrency(AccountPublic):
    currency: CurrencyPublic | None = None
    account_type: AccountTypePublic | None = None


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
