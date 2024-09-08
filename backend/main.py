from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from .database import get_session, create_db_and_tables, drop_db_and_tables
from .models import (
    Account,
    AccountPublic,
    AccountCreate,
    AccountUpdate,
    AccountPublicWithTypeAndCurrency,
    Currency,
    CurrencyPublic,
    AccountType,
    AccountTypePublic,
    Category,
    CategoryPublicWithSubcategories,
    SubCategory,
    SubCategoryPublicWithCategory,
    Transaction,
    TransactionPublic,
    TransactionCreate,
    TransactionUpdate,
    TransactionPublicWithCategorySubcategoryAndAccount,
)
from typing import List


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


@app.post("/accounts/", response_model=AccountPublic)
def create_account(*, session: Session = Depends(get_session), account: AccountCreate):
    db_account = Account.model_validate(account)
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account


@app.get("/accounts/", response_model=list[AccountPublicWithTypeAndCurrency])
def get_accounts(*, session: Session = Depends(get_session)):
    accounts: List[Account] = session.exec(select(Account)).all()
    accounts: List[Account] = sorted(accounts, key=lambda x: (x.created_at))
    return accounts


@app.get("/accounts/{account_id}", response_model=AccountPublicWithTypeAndCurrency)
def get_account(*, session: Session = Depends(get_session), account_id: int):
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@app.delete("/accounts/{account_id}")
def delete_account(*, session: Session = Depends(get_session), account_id: int):
    account = session.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    session.delete(account)
    session.commit()
    return {"ok": True}


@app.patch("/accounts/{account_id}", response_model=AccountPublic)
def update_account(
    *, session: Session = Depends(get_session), account_id: int, account: AccountUpdate
):
    db_account = session.get(Account, account_id)
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    account_data = account.model_dump(exclude_unset=True)
    for key, value in account_data.items():
        setattr(db_account, key, value)
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    return db_account


@app.get("/currencies/", response_model=list[CurrencyPublic])
def get_currencies(*, session: Session = Depends(get_session)):
    currencies = session.exec(select(Currency)).all()
    return currencies


@app.get("/account_types/", response_model=list[AccountTypePublic])
def get_account_types(*, session: Session = Depends(get_session)):
    account_types = session.exec(select(AccountType)).all()
    return account_types


@app.get("/categories/", response_model=list[CategoryPublicWithSubcategories])
def get_categories(*, session: Session = Depends(get_session)):
    categories = session.exec(select(Category)).all()
    return categories


@app.get("/sub_categories/", response_model=list[SubCategoryPublicWithCategory])
def get_sub_categories(*, session: Session = Depends(get_session)):
    sub_categories = session.exec(select(SubCategory)).all()
    return sub_categories


@app.get(
    "/transactions/",
    response_model=list[TransactionPublicWithCategorySubcategoryAndAccount],
)
def get_transactions(*, session: Session = Depends(get_session)):
    transactions: List[Transaction] = session.exec(select(Transaction)).all()
    transactions: List[Transaction] = sorted(
        transactions, key=lambda x: x.transaction_date
    )
    return transactions


@app.post("/transactions/", response_model=TransactionPublic)
def create_transaction(
    *, session: Session = Depends(get_session), transaction: TransactionCreate
):
    db_transaction = Transaction.model_validate(transaction)
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction


@app.get(
    "/transactions/{transaction_id}",
    response_model=TransactionPublicWithCategorySubcategoryAndAccount,
)
def get_transaction(*, session: Session = Depends(get_session), transaction_id: int):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@app.delete("/transactions/{transaction_id}")
def delete_transaction(*, session: Session = Depends(get_session), transaction_id: int):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    session.delete(transaction)
    session.commit()
    return {"ok": True}


@app.patch("/transactions/{transaction_id}", response_model=TransactionPublic)
def update_transaction(
    *,
    session: Session = Depends(get_session),
    transaction_id: int,
    transaction: TransactionUpdate,
):
    db_transaction = session.get(Transaction, transaction_id)
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    transaction_data = transaction.model_dump(exclude_unset=True)
    for key, value in transaction_data.items():
        setattr(db_transaction, key, value)
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction
