from datetime import date, datetime, timedelta
from typing import Dict, List, Tuple

import requests
import streamlit as st

API_URL: str = "http://localhost:8000"


@st.dialog("Update account")
def update_account(account: Dict) -> None:
    st.write(f"Account: {account}")
    st.rerun()


@st.dialog("Delete account")
def delete_account(account: Dict) -> None:
    st.write(f'Do you want to delete the "{account["name"]}" account?')
    if st.button("Delete"):
        requests.delete(url=f"{API_URL}/accounts/{account['id']}/")
        st.rerun()


@st.dialog("Update transaction")
def update_transaction(transaction: Dict) -> None:
    st.write(f"Transaction: {transaction}")
    st.rerun()


@st.dialog("Delete transaction")
def delete_transaction(transaction: Dict) -> None:
    st.write(f'Do you want to delete the "{transaction["id"]}" transaction?')
    if st.button("Delete"):
        requests.delete(url=f"{API_URL}/transactions/{transaction['id']}/")
        st.rerun()


def setup_page() -> None:
    page_title: str = "Wealth Tracker"
    page_icon: str = "💰"
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
    )
    st.title(f"{page_icon} {page_title}")


def date_range_filter_section() -> List[date]:
    st.header("Select a date range")
    current_date: date = date.today()
    first_day_of_current_month: date = date(current_date.year, current_date.month, 1)
    last_day_of_current_month: date = date(
        current_date.year, current_date.month + 1, 1
    ) - timedelta(days=1)
    st.date_input(
        "Select a date range",
        value=(first_day_of_current_month, last_day_of_current_month),
        key="date_range_filter",
        help="Select a date range to visualize",
    )
    return st.session_state.get("date_range_filter", None)


def get_date_range(date_range_filter: List[date]) -> Tuple[str, str]:
    start_date: str = date_range_filter[0].strftime("%Y-%m-%d")
    end_date: str = date_range_filter[1].strftime("%Y-%m-%d") + "T23:59:59"
    return start_date, end_date


def fetch_data(start_date: str, end_date: str) -> Dict:
    accounts: List[Dict] = requests.get(url=f"{API_URL}/accounts/").json()
    categories: List[Dict] = requests.get(url=f"{API_URL}/categories/").json()
    subcategories: List[Dict] = requests.get(url=f"{API_URL}/sub_categories/").json()
    accounts_balance: Dict = requests.get(
        url=f"{API_URL}/total_balance_per_account/"
    ).json()
    total_balance: Dict = requests.get(url=f"{API_URL}/total_balance/").json()
    transactions_between_dates: List[Dict] = requests.get(
        url=f"{API_URL}/transactions/?start_date={start_date}&end_date={end_date}"
    ).json()
    return {
        "accounts": accounts,
        "categories": categories,
        "subcategories": subcategories,
        "accounts_balance": accounts_balance,
        "total_balance": total_balance,
        "transactions_between_dates": transactions_between_dates,
    }


def render_tabs(data: Dict) -> None:
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Accounts", "Transactions", "Planned Transactions", "Budget"]
    )
    with tab1:
        render_accounts_tab(data)
    with tab2:
        render_transactions_tab(data)
    with tab3:
        st.header("Planned Transactions")
    with tab4:
        st.header("Budget")


def render_accounts_tab(data: Dict) -> None:
    st.header("Total Balance")
    st.metric("Current Total Balance", data["total_balance"]["total_balance"])

    st.header("Accounts")
    quantity_accounts: int = len(data["accounts_balance"])
    row = st.columns(1)
    for i, col in enumerate(row * quantity_accounts):
        tile = col.container(border=True)
        tile.header(data["accounts_balance"][i]["name"])
        tile.subheader(data["accounts_balance"][i]["account_type"])
        tile.metric(
            "Current balance",
            f"{data['accounts_balance'][i]['currency']} {data['accounts_balance'][i]['total_balance']}",
        )

        left, right = tile.columns(2)
        with left:
            if left.button(label="Edit", key=f"edit_account_{i}"):
                update_account(data["accounts_balance"][i])
        with right:
            if right.button(label="Delete", key=f"delete_account_{i}"):
                delete_account(data["accounts_balance"][i])

    st.header("Add a new account")


def render_transactions_tab(data: Dict) -> None:
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
            options=[account["name"] for account in data["accounts"]],
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
                for subcategory in data["subcategories"]
            ],
            help="Select the category and subcategory of the transaction",
        )
        description: str = st.text_input(
            "Description", help="Optional - Add a description to the transaction"
        )

        if st.form_submit_button("Add transaction"):
            new_category: str = category.split(" - ")[0]
            new_subcategory: str = category.split(" - ")[1]
            account_id: int = next(
                account["id"]
                for account in data["accounts"]
                if account_name == account["name"]
            )
            category_id: int = next(
                category["id"]
                for category in data["categories"]
                if new_category == category["name"]
            )
            subcategory_id: int = next(
                subcategory["id"]
                for subcategory in data["subcategories"]
                if new_subcategory == subcategory["name"]
            )

            payload: Dict = {
                "transaction_date": transaction_date.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                "account_id": account_id,
                "amount": amount,
                "category_id": category_id,
                "subcategory_id": subcategory_id,
                "description": description,
            }
            requests.post(url=f"{API_URL}/transactions/", json=payload)
            st.rerun()

    st.header("Transactions")
    quantity_transactions: int = len(data["transactions_between_dates"])
    row = st.columns(1)
    for i, col in enumerate(row * quantity_transactions):
        tile = col.container(border=True)
        tile.write(
            f"Account: {data['transactions_between_dates'][i]['account']['name']}"
        )
        tile.write(f"Date: {data['transactions_between_dates'][i]['transaction_date']}")
        tile.write(f"Amount: {data['transactions_between_dates'][i]['amount']}")
        tile.write(
            f"Category: {data['transactions_between_dates'][i]['category']['name']}"
        )
        tile.write(
            f"Subcategory: {data['transactions_between_dates'][i]['subcategory']['name']}"
        )
        tile.write(
            f"Description: {data['transactions_between_dates'][i]['description']}"
        )

        left, right = tile.columns(2)
        with left:
            if left.button(label="Edit", key=f"edit_transaction{i}"):
                update_transaction(data["transactions_between_dates"][i])
        with right:
            if right.button(label="Delete", key=f"delete_transaction{i}"):
                delete_transaction(data["transactions_between_dates"][i])


def main() -> None:
    setup_page()
    date_range_filter: List[date] = date_range_filter_section()
    start_date: str
    end_date: str
    start_date, end_date = get_date_range(date_range_filter)
    data: Dict = fetch_data(start_date, end_date)
    render_tabs(data)


if __name__ == "__main__":
    main()
