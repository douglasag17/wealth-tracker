from typing import List
from sqlmodel import SQLModel, Field, Relationship
from decimal import Decimal
from datetime import datetime


# Currency Model
class CurrencyBase(SQLModel):
    name: str = Field(nullable=False)  # COP, USD


class Currency(CurrencyBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    accounts: List["Account"] = Relationship(back_populates="currency")


class CurrencyPublic(CurrencyBase):
    id: int


# AccountType Model
class AccountTypeBase(SQLModel):
    type: str = Field(nullable=False)


class AccountType(AccountTypeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    accounts: List["Account"] = Relationship(back_populates="account_type")


class AccountTypePublic(AccountTypeBase):
    id: int


# Account Model
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
    transaction: List["Transaction"] = Relationship(back_populates="account")


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


# Category Model
class CategoryBase(SQLModel):
    name: str = Field(nullable=False)
    type: str = Field(nullable=False)  # income, expense


class Category(CategoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    subcategories: List["SubCategory"] = Relationship(back_populates="category")
    transactions: List["Transaction"] = Relationship(back_populates="category")


class CategoryPublic(CategoryBase):
    id: int


# SubCategory Model
class SubCategoryBase(SQLModel):
    name: str = Field(nullable=False)

    category_id: int = Field(default=None, foreign_key="category.id")


class SubCategory(SubCategoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    category: Category | None = Relationship(back_populates="subcategories")
    transactions: List["Transaction"] = Relationship(back_populates="subcategory")


class SubCategoryPublic(SubCategoryBase):
    id: int


class CategoryPublicWithSubcategories(CategoryPublic):
    subcategories: List[SubCategoryPublic] = []


class SubCategoryPublicWithCategory(SubCategoryPublic):
    category: CategoryPublic | None = None


# Transaction Model
class TransactionBase(SQLModel):
    amount: Decimal = Field(default=0, max_digits=50, decimal_places=2, nullable=False)
    description: str = Field(nullable=False)
    transaction_date: datetime | None = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    created_at: datetime | None = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
    )
    is_planned: bool = Field(default=False)
    is_paid: bool = Field(default=False)

    category_id: int = Field(default=None, foreign_key="category.id")
    subcategory_id: int = Field(default=None, foreign_key="subcategory.id")
    account_id: int = Field(default=None, foreign_key="account.id")


class Transaction(TransactionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    category: Category | None = Relationship(back_populates="transactions")
    subcategory: SubCategory | None = Relationship(back_populates="transactions")
    account: Account | None = Relationship(back_populates="transaction")


class TransactionPublic(TransactionBase):
    id: int


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(SQLModel):
    amount: Decimal | None = None
    description: str | None = None
    transaction_date: datetime | None = None
    is_planned: bool | None = None
    is_paid: bool | None = None
    subcategory_id: int | None = None
    account_id: int | None = None


class TransactionPublicWithCategorySubcategoryAndAccount(TransactionPublic):
    category: CategoryPublic | None = None
    subcategory: SubCategoryPublic | None = None
    account: AccountPublic | None = None


# MonthlyBudget Model
# class MonthlyBudget(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     subcategory_id: int = Field(default=None, foreign_key="subcategory.id")
#     year: int  # TODO:
#     month: int  # TODO:
#     budgeted: Decimal  # TODO:
