from sqlmodel import SQLModel, create_engine, Session
from .models import (
    Currency,
    AccountType,
    Account,
    Category,
    SubCategory,
    Transaction,
    MonthlyBudget,
)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    drop_db_and_tables()
    SQLModel.metadata.create_all(engine)
    create_currencies()
    create_account_types()
    create_accounts()
    create_categories()
    create_subcategories()
    create_transactions()
    create_monthly_budget()


def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)


def create_currencies():
    with Session(engine) as session:
        currency_1 = Currency(id=1, name="COP")
        currency_2 = Currency(id=2, name="USD")
        session.add(currency_1)
        session.add(currency_2)
        session.commit()


def create_account_types():
    with Session(engine) as session:
        account_type_1 = AccountType(id=1, type="savings account")
        account_type_2 = AccountType(id=2, type="credit card")
        account_type_3 = AccountType(id=3, type="cash")
        session.add(account_type_1)
        session.add(account_type_2)
        session.add(account_type_3)
        session.commit()


def create_accounts():
    with Session(engine) as session:
        account_1 = Account(
            id=1, name="bancolombia savings account", account_type_id=1, currency_id=1
        )
        account_2 = Account(
            id=2, name="bancolombia mastercard black", account_type_id=2, currency_id=1
        )
        account_3 = Account(id=3, name="usd cash", account_type_id=3, currency_id=2)
        session.add(account_1)
        session.add(account_2)
        session.add(account_3)
        session.commit()


def create_categories():
    with Session(engine) as session:
        category_1 = Category(id=1, name="income")
        category_2 = Category(id=2, name="housing")
        category_3 = Category(id=3, name="food")
        session.add(category_1)
        session.add(category_2)
        session.add(category_3)
        session.commit()


def create_subcategories():
    with Session(engine) as session:
        subcategory_1 = SubCategory(id=1, name="wage", category_id=1, type="must")
        subcategory_2 = SubCategory(id=2, name="rent", category_id=2, type="must")
        subcategory_3 = SubCategory(id=3, name="groceries", category_id=3, type="need")
        subcategory_4 = SubCategory(id=4, name="restaurant", category_id=3, type="want")
        session.add(subcategory_1)
        session.add(subcategory_2)
        session.add(subcategory_3)
        session.add(subcategory_4)
        session.commit()


def create_transactions():
    with Session(engine) as session:
        pass


def create_monthly_budget():
    with Session(engine) as session:
        pass
