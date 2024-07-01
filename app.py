import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import pandas as pd

# Database setup
DATABASE_URL = "sqlite:///finance.db"

Base = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    description = Column(String)
    category = Column(String)
    amount = Column(Float)
    type = Column(String)  # 'expense' or 'income'
    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship("Account")

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Function to add transaction
def add_transaction(date, description, category, amount, type, account_id):
    new_transaction = Transaction(date=date, description=description, category=category, amount=amount, type=type, account_id=account_id)
    session.add(new_transaction)
    session.commit()

# Function to view all transactions
def view_transactions():
    transactions = session.query(Transaction).all()
    return transactions

# Function to delete transaction
def delete_transaction(transaction_id):
    transaction = session.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction:
        session.delete(transaction)
        session.commit()

# Function to update transaction
def update_transaction(transaction_id, date, description, category, amount, type, account_id):
    transaction = session.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction:
        transaction.date = date
        transaction.description = description
        transaction.category = category
        transaction.amount = amount
        transaction.type = type
        transaction.account_id = account_id
        session.commit()

# Function to add account
def add_account(name):
    new_account = Account(name=name)
    session.add(new_account)
    session.commit()

# Function to view all accounts
def view_accounts():
    accounts = session.query(Account).all()
    return accounts

# Streamlit app
st.title('Finance Tracker')

menu = ['Add Transaction', 'View Transactions', 'Delete Transaction', 'Modify Transaction', 'Add Account', 'View Accounts']
choice = st.sidebar.selectbox('Menu', menu)

if choice == 'Add Transaction':
    st.subheader('Add New Transaction')
    date = st.date_input('Date')
    description = st.text_input('Description')
    category = st.text_input('Category')
    amount = st.number_input('Amount', min_value=0.0, format="%.2f")
    type = st.selectbox('Type', ['expense', 'income'])
    accounts = view_accounts()
    account = st.selectbox('Account', [acc.name for acc in accounts])

    if st.button('Add Transaction'):
        account_id = next(acc.id for acc in accounts if acc.name == account)
        add_transaction(date, description, category, amount, type, account_id)
        st.success(f'Added {type}: {description} - {amount}')

elif choice == 'View Transactions':
    st.subheader('View All Transactions')
    transactions = view_transactions()

    if transactions:
        df = pd.DataFrame([(t.id, t.date, t.description, t.category, t.amount, t.type, t.account.name) for t in transactions],
                          columns=['ID', 'Date', 'Description', 'Category', 'Amount', 'Type', 'Account'])
        st.dataframe(df)
    else:
        st.write('No transactions found.')

elif choice == 'Delete Transaction':
    st.subheader('Delete a Transaction')
    transaction_id = st.number_input('Transaction ID', min_value=1)

    if st.button('Delete Transaction'):
        delete_transaction(transaction_id)
        st.success(f'Deleted transaction with ID: {transaction_id}')

elif choice == 'Modify Transaction':
    st.subheader('Modify a Transaction')
    transaction_id = st.number_input('Transaction ID', min_value=1)
    transaction = session.query(Transaction).filter(Transaction.id == transaction_id).first()

    if transaction:
        date = st.date_input('Date', value=transaction.date)
        description = st.text_input('Description', value=transaction.description)
        category = st.text_input('Category', value=transaction.category)
        amount = st.number_input('Amount', min_value=0.0, value=transaction.amount, format="%.2f")
        type = st.selectbox('Type', ['expense', 'income'], index=['expense', 'income'].index(transaction.type))
        accounts = view_accounts()
        account = st.selectbox('Account', [acc.name for acc in accounts], index=[acc.id for acc in accounts].index(transaction.account_id))

        if st.button('Modify Transaction'):
            account_id = next(acc.id for acc in accounts if acc.name == account)
            update_transaction(transaction_id, date, description, category, amount, type, account_id)
            st.success(f'Updated transaction with ID: {transaction_id}')
    else:
        st.write('Transaction not found.')

elif choice == 'Add Account':
    st.subheader('Add New Account')
    account_name = st.text_input('Account Name')

    if st.button('Add Account'):
        add_account(account_name)
        st.success(f'Added account: {account_name}')

elif choice == 'View Accounts':
    st.subheader('View All Accounts')
    accounts = view_accounts()

    if accounts:
        df = pd.DataFrame([(acc.id, acc.name) for acc in accounts], columns=['ID', 'Account Name'])
        st.dataframe(df)
    else:
        st.write('No accounts found.')

# Close the session at the end
session.close()
