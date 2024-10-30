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
    CurrencyCreate,
    CurrencyUpdate,
    AccountType,
    AccountTypePublic,
    AccountTypeCreate,
    AccountTypeUpdate,
    Category,
    CategoryPublic,
    CategoryCreate,
    CategoryUpdate,
    CategoryPublicWithSubcategories,
    SubCategory,
    SubCategoryPublic,
    SubCategoryCreate,
    SubCategoryUpdate,
    SubCategoryPublicWithCategory,
    Transaction,
    TransactionPublic,
    TransactionCreate,
    TransactionUpdate,
    TransactionPublicWithCategorySubcategoryAndAccount,
    PlannedTransaction,
    PlannedTransactionPublic,
    PlannedTransactionCreate,
    PlannedTransactionUpdate,
    Budget,
    BudgetPublic,
    BudgetCreate,
    BudgetUpdate,
)
from typing import List, Optional
from datetime import date, timedelta


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


@app.post("/currencies/", response_model=CurrencyPublic)
def create_currency(
    *, session: Session = Depends(get_session), currency: CurrencyCreate
):
    db_currency = Currency.model_validate(currency)
    session.add(db_currency)
    session.commit()
    session.refresh(db_currency)
    return db_currency


@app.get("/currencies/", response_model=list[CurrencyPublic])
def get_currencies(*, session: Session = Depends(get_session)):
    currencies = session.exec(select(Currency)).all()
    return currencies


@app.get("/currencies/{currency_id}", response_model=CurrencyPublic)
def get_currency(*, session: Session = Depends(get_session), currency_id: int):
    currency = session.get(Currency, currency_id)
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    return currency


@app.delete("/currencies/{currency_id}")
def delete_currency(*, session: Session = Depends(get_session), currency_id: int):
    currency = session.get(Currency, currency_id)
    if not currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    session.delete(currency)
    session.commit()
    return {"ok": True}


@app.patch("/currencies/{currency_id}", response_model=CurrencyPublic)
def update_currency(
    *,
    session: Session = Depends(get_session),
    currency_id: int,
    currency: CurrencyUpdate,
):
    db_currency = session.get(Currency, currency_id)
    if not db_currency:
        raise HTTPException(status_code=404, detail="Currency not found")
    currency_data = currency.model_dump(exclude_unset=True)
    for key, value in currency_data.items():
        setattr(db_currency, key, value)
    session.add(db_currency)
    session.commit()
    session.refresh(db_currency)
    return db_currency


@app.post("/account_types/", response_model=AccountTypePublic)
def create_account_type(
    *, session: Session = Depends(get_session), account_type: AccountTypeCreate
):
    db_account_type = AccountType.model_validate(account_type)
    session.add(db_account_type)
    session.commit()
    session.refresh(db_account_type)
    return db_account_type


@app.get("/account_types/", response_model=list[AccountTypePublic])
def get_account_types(*, session: Session = Depends(get_session)):
    account_types = session.exec(select(AccountType)).all()
    return account_types


@app.get("/account_types/{account_type_id}", response_model=AccountTypePublic)
def get_account_type(*, session: Session = Depends(get_session), account_type_id: int):
    account_type = session.get(AccountType, account_type_id)
    if not account_type:
        raise HTTPException(status_code=404, detail="Account Type not found")
    return account_type


@app.delete("/account_types/{account_type_id}")
def delete_account_type(
    *, session: Session = Depends(get_session), account_type_id: int
):
    account_type = session.get(AccountType, account_type_id)
    if not account_type:
        raise HTTPException(status_code=404, detail="Account Type not found")
    session.delete(account_type)
    session.commit()
    return {"ok": True}


@app.patch("/account_types/{account_type_id}", response_model=AccountTypePublic)
def update_account_type(
    *,
    session: Session = Depends(get_session),
    account_type_id: int,
    account_type: AccountTypeUpdate,
):
    db_account_type = session.get(AccountType, account_type_id)
    if not db_account_type:
        raise HTTPException(status_code=404, detail="Account Type not found")
    account_type_data = account_type.model_dump(exclude_unset=True)
    for key, value in account_type_data.items():
        setattr(db_account_type, key, value)
    session.add(db_account_type)
    session.commit()
    session.refresh(db_account_type)
    return db_account_type


@app.post("/categories/", response_model=CategoryPublic)
def create_category(
    *, session: Session = Depends(get_session), category: CategoryCreate
):
    db_category = Category.model_validate(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@app.get("/categories/", response_model=list[CategoryPublicWithSubcategories])
def get_categories(*, session: Session = Depends(get_session)):
    categories = session.exec(select(Category)).all()
    return categories


@app.get("/categories/{category_id}", response_model=CategoryPublicWithSubcategories)
def get_category(*, session: Session = Depends(get_session), category_id: int):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.delete("/categories/{category_id}")
def delete_category(*, session: Session = Depends(get_session), category_id: int):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"ok": True}


@app.patch("/categories/{category_id}", response_model=CategoryPublic)
def update_category(
    *,
    session: Session = Depends(get_session),
    category_id: int,
    category: CategoryUpdate,
):
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    category_data = category.model_dump(exclude_unset=True)
    for key, value in category_data.items():
        setattr(db_category, key, value)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@app.post("/sub_categories/", response_model=SubCategoryPublic)
def create_sub_category(
    *, session: Session = Depends(get_session), sub_category: SubCategoryCreate
):
    db_sub_category = SubCategory.model_validate(sub_category)
    session.add(db_sub_category)
    session.commit()
    session.refresh(db_sub_category)
    return db_sub_category


@app.get("/sub_categories/", response_model=list[SubCategoryPublicWithCategory])
def get_sub_categories(*, session: Session = Depends(get_session)):
    sub_categories = session.exec(select(SubCategory)).all()
    return sub_categories


@app.get(
    "/sub_categories/{sub_category_id}", response_model=SubCategoryPublicWithCategory
)
def get_sub_category(*, session: Session = Depends(get_session), sub_category_id: int):
    sub_category = session.get(SubCategory, sub_category_id)
    if not sub_category:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    return sub_category


@app.delete("/sub_categories/{sub_category_id}")
def delete_sub_category(
    *, session: Session = Depends(get_session), sub_category_id: int
):
    sub_category = session.get(SubCategory, sub_category_id)
    if not sub_category:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    session.delete(sub_category)
    session.commit()
    return {"ok": True}


@app.patch("/sub_categories/{sub_category_id}", response_model=SubCategoryPublic)
def update_sub_category(
    *,
    session: Session = Depends(get_session),
    sub_category_id: int,
    sub_category: SubCategoryUpdate,
):
    db_sub_category = session.get(SubCategory, sub_category_id)
    if not db_sub_category:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    sub_category_data = sub_category.model_dump(exclude_unset=True)
    for key, value in sub_category_data.items():
        setattr(db_sub_category, key, value)
    session.add(db_sub_category)
    session.commit()
    session.refresh(db_sub_category)
    return db_sub_category


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
    "/transactions/",
    response_model=list[TransactionPublicWithCategorySubcategoryAndAccount],
)
def get_transactions(
    *,
    start_date: Optional[date] = None,
    end_date: Optional[date] = date(date.today().year, date.today().month + 1, 1)
    - timedelta(days=1),
    session: Session = Depends(get_session),
):
    if start_date:
        transactions: List[Transaction] = session.exec(
            select(Transaction)
            .where(Transaction.transaction_date >= start_date)
            .where(Transaction.transaction_date <= end_date)
        ).all()
    else:
        transactions: List[Transaction] = session.exec(
            select(Transaction).where(Transaction.transaction_date <= end_date)
        ).all()
    transactions: List[Transaction] = sorted(
        transactions, key=lambda x: x.transaction_date
    )
    return transactions


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


@app.post("/planned_transactions/", response_model=PlannedTransactionPublic)
def create_planned_transaction(
    *,
    session: Session = Depends(get_session),
    planned_transaction: PlannedTransactionCreate,
):
    db_planned_transaction = PlannedTransaction.model_validate(planned_transaction)
    session.add(db_planned_transaction)
    session.commit()
    session.refresh(db_planned_transaction)
    return db_planned_transaction


@app.get("/planned_transactions/", response_model=list[PlannedTransactionPublic])
def get_planned_transactions(
    *,
    start_date: Optional[date] = None,
    end_date: Optional[date] = date(date.today().year, date.today().month + 1, 1)
    - timedelta(days=1),
    session: Session = Depends(get_session),
):
    if start_date:
        planned_transactions: List[PlannedTransaction] = session.exec(
            select(PlannedTransaction)
            .where(PlannedTransaction.transaction_date >= start_date)
            .where(PlannedTransaction.transaction_date <= end_date)
        ).all()
    else:
        planned_transactions: List[PlannedTransaction] = session.exec(
            select(PlannedTransaction).where(
                PlannedTransaction.transaction_date <= end_date
            )
        ).all()
    planned_transactions: List[PlannedTransaction] = sorted(
        planned_transactions, key=lambda x: x.transaction_date
    )
    return planned_transactions


@app.get(
    "/planned_transactions/{planned_transaction_id}",
    response_model=PlannedTransactionPublic,
)
def get_planned_transaction(
    *, session: Session = Depends(get_session), planned_transaction_id: int
):
    planned_transaction = session.get(PlannedTransaction, planned_transaction_id)
    if not planned_transaction:
        raise HTTPException(status_code=404, detail="Planned Transaction not found")
    return planned_transaction


@app.delete("/planned_transactions/{planned_transaction_id}")
def delete_planned_transaction(
    *, session: Session = Depends(get_session), planned_transaction_id: int
):
    planned_transaction = session.get(PlannedTransaction, planned_transaction_id)
    if not planned_transaction:
        raise HTTPException(status_code=404, detail="Planned Transaction not found")
    session.delete(planned_transaction)
    session.commit()
    return {"ok": True}


@app.patch(
    "/planned_transactions/{planned_transaction_id}",
    response_model=PlannedTransactionPublic,
)
def update_planned_transaction(
    *,
    session: Session = Depends(get_session),
    planned_transaction_id: int,
    planned_transaction: PlannedTransactionUpdate,
):
    db_planned_transaction = session.get(PlannedTransaction, planned_transaction_id)
    if not db_planned_transaction:
        raise HTTPException(status_code=404, detail="Planned Transaction not found")
    planned_transaction_data = planned_transaction.model_dump(exclude_unset=True)
    for key, value in planned_transaction_data.items():
        setattr(db_planned_transaction, key, value)
    session.add(db_planned_transaction)
    session.commit()
    session.refresh(db_planned_transaction)
    return db_planned_transaction


@app.post("/budgets/", response_model=BudgetPublic)
def create_budget(*, session: Session = Depends(get_session), budget: BudgetCreate):
    db_budget = Budget.model_validate(budget)
    session.add(db_budget)
    session.commit()
    session.refresh(db_budget)
    return db_budget


@app.get("/budgets/", response_model=list[BudgetPublic])
def get_budgets(*, session: Session = Depends(get_session)):
    budgets = session.exec(select(Budget)).all()
    return budgets


@app.get("/budgets/{budget_id}", response_model=BudgetPublic)
def get_budget(*, session: Session = Depends(get_session), budget_id: int):
    budget = session.get(Budget, budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget


@app.delete("/budgets/{budget_id}")
def delete_budget(*, session: Session = Depends(get_session), budget_id: int):
    budget = session.get(Budget, budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    session.delete(budget)
    session.commit()
    return {"ok": True}


@app.patch("/budgets/{budget_id}", response_model=BudgetPublic)
def update_budget(
    *,
    session: Session = Depends(get_session),
    budget_id: int,
    budget: BudgetUpdate,
):
    db_budget = session.get(Budget, budget_id)
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    budget_data = budget.model_dump(exclude_unset=True)
    for key, value in budget_data.items():
        setattr(db_budget, key, value)
    session.add(db_budget)
    session.commit()
    session.refresh(db_budget)
    return db_budget
