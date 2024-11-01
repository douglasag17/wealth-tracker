from datetime import date, datetime, timedelta
from typing import Dict, List

import requests
import streamlit as st

API_URL = "http://localhost:8000"


@st.dialog("Update account")
def update_account(account: Dict):
    st.write(f"Account: {account}")
    st.rerun()


@st.dialog("Delete account")
def delete_account(account: Dict):
    st.write(f'Do you want to delete the "{account["name"]}" account?')
    if st.button("Delete"):
        requests.delete(url=f"{API_URL}/accounts/{account['id']}/")
        st.rerun()


@st.dialog("Update transaction")
def update_transaction(transaction: Dict):
    st.write(f"Transaction: {transaction}")
    st.rerun()


@st.dialog("Delete transaction")
def delete_transaction(transaction: Dict):
    st.write(f'Do you want to delete the "{transaction["id"]}" transaction?')
    if st.button("Delete"):
        requests.delete(url=f"{API_URL}/transactions/{transaction['id']}/")
        st.rerun()


def main():
    # Set up page
    page_title: str = "Wealth Tracker"
    page_icon: str = "💰"
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        # layout="wide",
    )
    st.title(f"{page_icon} {page_title}")

    # FIXME: replace this with a dropdown of options (e.g. last month, last 3 months, last year) or a year-month picker
    # Date range filter
    st.header("Select a date range")
    current_date = date.today()
    first_day_of_current_month = date(current_date.year, current_date.month, 1)
    last_day_of_current_month = date(
        current_date.year, current_date.month + 1, 1
    ) - timedelta(days=1)
    st.date_input(
        "Select a date range",
        value=(first_day_of_current_month, last_day_of_current_month),
        key="date_range_filter",
        help="Select a date range to visualize",
    )
    date_range_filter: List[date] = st.session_state.get("date_range_filter", None)
    start_date: str = date_range_filter[0].strftime("%Y-%m-%d")
    end_date: str = date_range_filter[1].strftime("%Y-%m-%d") + "T23:59:59"

    # Data
    accounts: List[Dict] = requests.get(url=f"{API_URL}/accounts/").json()
    categories: List[Dict] = requests.get(url=f"{API_URL}/categories/").json()
    subcategories: List[Dict] = requests.get(url=f"{API_URL}/sub_categories/").json()
    accounts_balance: List[Dict] = requests.get(
        url=f"{API_URL}/total_balance_per_account/"
    ).json()
    total_balance: Dict = requests.get(url=f"{API_URL}/total_balance/").json()
    # transactions_until_end_date: List[Dict] = requests.get(
    #     url=f"{API_URL}/transactions/?end_date={end_date}"
    # ).json()
    transactions_between_dates: List[Dict] = requests.get(
        url=f"{API_URL}/transactions/?start_date={start_date}&end_date={end_date}"
    ).json()

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Accounts", "Transactions", "Planned Transactions", "Budget"]
    )
    with tab1:
        # Total Balance
        st.header("Total Balance")
        st.metric("Current Total Balance", total_balance["total_balance"])

        # Accounts
        st.header("Accounts")
        quantity_accounts: int = len(accounts_balance)
        row = st.columns(1)
        for i, col in enumerate(row * quantity_accounts):
            tile = col.container(border=True)
            tile.header(accounts_balance[i]["name"])
            tile.subheader(accounts_balance[i]["account_type"])
            tile.metric(
                "Current balance",
                f"{accounts_balance[i]["currency"]} {accounts_balance[i]["total_balance"]}",
            )

            # Buttons
            left, right = tile.columns(2)
            with left:
                if left.button(label="Edit", key=f"edit_account_{i}"):
                    update_account(accounts_balance[i])
            with right:
                if right.button(label="Delete", key=f"delete_account_{i}"):
                    delete_account(accounts_balance[i])

        # Form to create a new account
        st.header("Add a new account")

    with tab2:
        # Add a new transaction
        st.header("Add a new transaction")
        with st.form("form_add_transaction", clear_on_submit=True, border=True):
            transaction_date: datetime = st.date_input(
                "Transaction Date",
                value=datetime.now(),
                format="YYYY-MM-DD",
                help="Select the date and time of the transaction",
            )
            account_name: str = st.selectbox(
                "Account",
                options=[account["name"] for account in accounts],
                help="Select the account where the transaction belongs",
            )
            amount: float = st.number_input(
                "Amount",
                help="Add the amount of the transaction. Currency depends on the selected account",
            )
            category: str = st.selectbox(
                "Category",
                options=[
                    f"{subcategory['category']['name']} - {subcategory['name']}"
                    for subcategory in subcategories
                ],
                help="Select the category and subcategory of the transaction",
            )
            description: str = st.text_input(
                "Description", help="Optional - Add a description to the transaction"
            )

            if st.form_submit_button("Add transaction"):
                new_category: str = category.split(" - ")[0]
                new_subcategory: str = category.split(" - ")[1]
                for account in accounts:
                    if account_name == account["name"]:
                        account_id: int = account["id"]
                for category in categories:
                    if new_category == category["name"]:
                        category_id: int = category["id"]
                for subcategory in subcategories:
                    if new_subcategory == subcategory["name"]:
                        subcategory_id: int = subcategory["id"]

                payload: Dict = {
                    "transaction_date": transaction_date.strftime(
                        "%Y-%m-%dT%H:%M:%S.%f"
                    ),
                    "account_id": account_id,
                    "amount": amount,
                    "category_id": category_id,
                    "subcategory_id": subcategory_id,
                    "description": description,
                }
                requests.post(url=f"{API_URL}/transactions/", json=payload)
                st.rerun()

        # Transactions
        st.header("Transactions")
        quantity_transactions: int = len(transactions_between_dates)
        row = st.columns(1)
        for i, col in enumerate(row * quantity_transactions):
            tile = col.container(border=True)
            tile.write(f"Account: {transactions_between_dates[i]['account']['name']}")
            tile.write(f"Date: {transactions_between_dates[i]["transaction_date"]}")
            tile.write(f"Amount: {transactions_between_dates[i]["amount"]}")
            tile.write(f"Category: {transactions_between_dates[i]["category"]["name"]}")
            tile.write(
                f"Subcategory: {transactions_between_dates[i]['subcategory']['name']}"
            )
            tile.write(f"Description: {transactions_between_dates[i]['description']}")

            # Buttons
            left, right = tile.columns(2)
            with left:
                if left.button(label="Edit", key=f"edit_transaction{i}"):
                    update_transaction(transactions_between_dates[i])
            with right:
                if right.button(label="Delete", key=f"delete_transaction{i}"):
                    delete_transaction(transactions_between_dates[i])

    with tab3:
        # Planned Transactions
        st.header("Planned Transactions")

    with tab4:
        # Budget
        st.header("Budget")


if __name__ == "__main__":
    main()
