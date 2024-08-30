import streamlit as st
import requests
from utils import set_up_page, API_URL
import pandas as pd
from typing import List, Dict


def get_transactions():
    st.subheader("Transactions")

    # Getting data from API
    transactions: List[Dict] = requests.get(url=f"{API_URL}/transactions/").json()
    accounts: List[Dict] = requests.get(url=f"{API_URL}/accounts/").json()
    categories: List[Dict] = requests.get(url=f"{API_URL}/categories/").json()
    subcategories: List[Dict] = requests.get(url=f"{API_URL}/sub_categories/").json()

    # Creating Dataframe
    transactions_df = pd.json_normalize(transactions)
    transactions_df["transaction_date"] = pd.to_datetime(
        transactions_df["transaction_date"], infer_datetime_format=True
    )

    # Writing table
    column_config: Dict = {
        "transaction_date": st.column_config.DatetimeColumn(
            "Transaction Date", format="YYYY-MM-DD HH:mm:ss.SSS"
        ),
        "account.name": st.column_config.SelectboxColumn(
            "Account",
            required=True,
            options=[account["name"] for account in accounts],
        ),
        "amount": st.column_config.NumberColumn("Amount", required=True),
        "category.name": st.column_config.SelectboxColumn(
            "Category",
            required=True,
            options=[category["name"] for category in categories],
        ),
        "subcategory.name": st.column_config.SelectboxColumn(
            "Subcategory",
            required=True,
            options=[subcategory["name"] for subcategory in subcategories],
        ),
        "description": st.column_config.TextColumn("Description"),
    }
    column_order = (
        "transaction_date",
        "account.name",
        "amount",
        "category.name",
        "subcategory.name",
        "description",
    )

    with st.form("form_edit_transactions"):
        st.data_editor(
            transactions_df,
            key="edited_transactions_df",
            column_config=column_config,
            column_order=column_order,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",
        )

        # Submit button
        if st.form_submit_button("Submit"):
            pass


def main():
    set_up_page()
    get_transactions()
    # TODO: Add a form to create new accounts with a better UI
    # https://docs.streamlit.io/develop/concepts/architecture/forms
    # https://docs.streamlit.io/develop/api-reference/execution-flow/st.dialog


if __name__ == "__main__":
    main()
