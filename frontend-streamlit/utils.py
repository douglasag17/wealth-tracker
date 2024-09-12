import streamlit as st
from datetime import date, timedelta
from typing import List, Dict
import requests
import pandas as pd


API_URL: str = "http://127.0.0.1:8000"


def set_up_page():
    page_title: str = "Wealth Tracker"
    page_icon: str = "💰"
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        # layout="wide",
        initial_sidebar_state="auto",
    )
    st.title(f"{page_icon} {page_title}")
    set_up_sidebar()


def set_up_sidebar():
    st.sidebar.title("Filters")

    # Date range filter
    today = date.today()
    first_day_of_month = date(today.year, today.month, 1)
    last_day_of_month = date(today.year, today.month + 1, 1) - timedelta(days=1)
    st.sidebar.date_input(
        "Select a date range",
        value=(first_day_of_month, last_day_of_month),
        key="date_range_filter",
        help="Select a date range to visualize",
    )


def get_data_from_api() -> Dict[str, List[Dict]]:
    # Getting date range filter
    date_range_filter: List[date] = st.session_state.get("date_range_filter", None)
    if date_range_filter is None:
        st.warning("Select a complete date range", icon="⚠️")
        st.stop()
    start_date: str = ""
    end_date: str = ""
    if len(date_range_filter) == 2:
        start_date = date_range_filter[0].strftime("%Y-%m-%d")
        end_date = date_range_filter[1].strftime("%Y-%m-%d")

    # Getting data from API
    accounts: List[Dict] = requests.get(url=f"{API_URL}/accounts/").json()
    currencies: List[Dict] = requests.get(url=f"{API_URL}/currencies/").json()
    account_types: List[Dict] = requests.get(url=f"{API_URL}/account_types/").json()
    categories: List[Dict] = requests.get(url=f"{API_URL}/categories/").json()
    subcategories: List[Dict] = requests.get(url=f"{API_URL}/sub_categories/").json()

    transactions_until_end_date: List[Dict] = []
    if end_date != "":
        transactions_until_end_date = requests.get(
            url=f"{API_URL}/transactions/?end_date={end_date}"
        ).json()
    elif len(transactions_until_end_date) == 0:
        st.warning("Select a complete date range", icon="⚠️")
        st.stop()

    transactions_between_date_range: List[Dict] = []
    if start_date != "" and end_date != "":
        transactions_between_date_range = requests.get(
            url=f"{API_URL}/transactions/?start_date={start_date}&end_date={end_date}"
        ).json()
    elif len(transactions_between_date_range) == 0:
        st.warning("Select a complete date range", icon="⚠️")
        st.stop()

    return {
        "accounts": accounts,
        "currencies": currencies,
        "account_types": account_types,
        "categories": categories,
        "subcategories": subcategories,
        "transactions_until_end_date": transactions_until_end_date,
        "transactions_between_date_range": transactions_between_date_range,
    }


def create_transactions_until_end_date_df(data: Dict[str, List[Dict]]) -> pd.DataFrame:
    transactions_until_end_date_df: pd.DataFrame = pd.json_normalize(
        data["transactions_until_end_date"]
    )
    transactions_until_end_date_df["transaction_date"] = pd.to_datetime(
        transactions_until_end_date_df["transaction_date"]
    )
    transactions_until_end_date_df["amount"] = transactions_until_end_date_df[
        "amount"
    ].astype(float)
    transactions_until_end_date_df["amount_with_sign"] = (
        transactions_until_end_date_df.apply(
            lambda x: x["amount"] if x["category.type"] == "income" else -x["amount"],
            axis=1,
        )
    )
    transactions_until_end_date_df["running_balance"] = (
        transactions_until_end_date_df.groupby(
            "account_id"
        )["amount_with_sign"].cumsum()
    )
    return transactions_until_end_date_df


def create_transactions_between_date_range_df(
    data: Dict[str, List[Dict]], transactions_until_end_date_df: pd.DataFrame
) -> pd.DataFrame:
    transactions_between_date_range_df: pd.DataFrame = pd.json_normalize(
        data["transactions_between_date_range"]
    )
    transactions_between_date_range_df["transaction_date"] = pd.to_datetime(
        transactions_between_date_range_df["transaction_date"]
    )
    transactions_between_date_range_df["amount"] = transactions_between_date_range_df[
        "amount"
    ].astype(float)
    transactions_between_date_range_df["running_balance"] = (
        transactions_between_date_range_df[
            "id"
        ].map(transactions_until_end_date_df.set_index("id")["running_balance"])
    )
    transactions_between_date_range_df["categories_with_subcategories"] = (
        transactions_between_date_range_df["category.name"]
        + " - "
        + transactions_between_date_range_df["subcategory.name"]
    )
    return transactions_between_date_range_df


def create_accounts_df(
    data: Dict[str, List[Dict]], transactions_until_end_date_df: pd.DataFrame
) -> pd.DataFrame:
    accounts_df: pd.DataFrame = pd.json_normalize(data["accounts"])
    transactions_aggregated: pd.DataFrame = transactions_until_end_date_df.groupby(
        "account_id"
    )["amount_with_sign"].sum()
    accounts_df["balance"] = accounts_df["id"].map(transactions_aggregated).fillna(0)
    accounts_df["balance_cop"] = accounts_df.apply(
        lambda x: x["balance"] if x["currency.name"] == "COP" else x["balance"] * 4000,
        axis=1,
    )
    return accounts_df


def get_dataframes(data: Dict[str, List[Dict]]) -> Dict[str, pd.DataFrame]:
    transactions_until_end_date_df = create_transactions_until_end_date_df(data)
    transactions_between_date_range_df = create_transactions_between_date_range_df(
        data, transactions_until_end_date_df
    )
    accounts_df = create_accounts_df(data, transactions_until_end_date_df)

    return {
        "accounts_df": accounts_df,
        "transactions_until_end_date_df": transactions_until_end_date_df,
        "transactions_between_date_range_df": transactions_between_date_range_df,
    }
