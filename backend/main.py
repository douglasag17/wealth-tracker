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
)


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
    accounts = session.exec(select(Account)).all()
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
