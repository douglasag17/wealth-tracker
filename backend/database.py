from sqlmodel import SQLModel, create_engine, Session
from .models import Account, Transaction


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def create_accounts():
    with Session(engine) as session:
        account_1 = Account(id=1, name="savings account")
        session.add(account_1)
        session.commit()
