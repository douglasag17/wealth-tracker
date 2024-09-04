import streamlit as st
import requests
from utils import set_up_page, API_URL
import pandas as pd
from typing import List, Dict
from datetime import datetime, date


def get_accounts():
    st.subheader("Accounts")

    # Getting data from API
    accounts: List[Dict] = requests.get(url=f"{API_URL}/accounts/").json()
    currencies: List[Dict] = requests.get(url=f"{API_URL}/currencies/").json()
    account_types: List[Dict] = requests.get(url=f"{API_URL}/account_types/").json()
    transactions: List[Dict] = requests.get(url=f"{API_URL}/transactions/").json()

    # Creating Dataframe
    accounts_df: pd.DataFrame = pd.json_normalize(accounts)
    transactions_df: pd.DataFrame = pd.json_normalize(transactions)
    transactions_df["transaction_date"] = pd.to_datetime(
        transactions_df["transaction_date"]
    )
    transactions_df["amount"] = transactions_df["amount"].astype(float)

    # Filtering data to show only the transactions up until the end date selected
    date_range_filter: List[date] = st.session_state["date_range_filter"]
    if len(date_range_filter) == 2:
        end_date: date = date_range_filter[1]
        transactions_df = transactions_df[
            transactions_df["transaction_date"]
            <= datetime.combine(end_date, datetime.max.time())
        ]

    # join accounts_df with transactions_df to get the total balance of each account, if category is income, add amount, otherwise, subtract amount. If the balance is None, set it to 0
    accounts_df["balance"] = transactions_df.groupby(
        by="account_id", group_keys=False
    ).apply(
        lambda x: x["amount"].sum()
        if x["category.name"].iloc[0] == "income"
        else -x["amount"].sum()
    )
    accounts_df["balance"] = accounts_df["balance"].fillna(0)

    # accounts_df = accounts_df.merge(
    #     transactions_df,
    #     how="left",
    #     left_on="id",
    #     right_on="account_id",
    #     suffixes=("", "_transaction"),
    #     validate="one_to_many",
    # )
    # accounts_df["balance"] = accounts_df.groupby("id")["amount"].transform("sum")
    # accounts_df["balance"] = accounts_df["balance"].fillna(0)

    # Ordering rows
    accounts_df.sort_values(
        by=["account_type.type", "currency.name", "name"],
        inplace=True,
        ignore_index=True,
    )

    # Writing table
    column_config: Dict = {
        "name": st.column_config.TextColumn(
            "Name", required=True, help="Add the name of the account"
        ),
        "currency.name": st.column_config.SelectboxColumn(
            "Currency",
            required=True,
            help="Select the currency of the account",
            options=[currency["name"] for currency in currencies],
        ),
        "account_type.type": st.column_config.SelectboxColumn(
            "Type",
            required=True,
            help="Select the type of the account",
            options=[account_type["type"] for account_type in account_types],
        ),
        "balance": st.column_config.NumberColumn(
            "Current Balance",
            required=False,
            default=0.0,
            help="Shows the current balance of the account",
        ),
    }
    column_order = ("name", "account_type.type", "currency.name", "balance")
    disabled: list = ["created_at", "updated_at", "balance"]

    with st.form("form_edit_accounts"):
        st.data_editor(
            accounts_df,
            key="edited_accounts_df",
            column_config=column_config,
            column_order=column_order,
            disabled=disabled,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",
        )

        # Submit button
        if st.form_submit_button("Save changes"):
            st.write(st.session_state["edited_accounts_df"])
            insert_new_accounts(currencies, account_types)
            update_accounts(accounts, currencies, account_types)
            delete_accounts(accounts)

            # Refresh app
            st.rerun()


def insert_new_accounts(currencies: List[Dict], account_types: List[Dict]):
    added_accounts: List[Dict] = st.session_state["edited_accounts_df"]["added_rows"]
    if added_accounts:
        for i, new_account in enumerate(added_accounts):
            for currency in currencies:
                if new_account["currency.name"] == currency["name"]:
                    added_accounts[i]["currency_id"] = currency["id"]
            for account_type in account_types:
                if new_account["account_type.type"] == account_type["type"]:
                    added_accounts[i]["account_type_id"] = account_type["id"]
            # api call to add new accounts
            payload: Dict = {
                "name": new_account["name"],
                "account_type_id": new_account["account_type_id"],
                "currency_id": new_account["currency_id"],
            }
            requests.post(url=f"{API_URL}/accounts/", json=payload)


def update_accounts(
    accounts: List[Dict], currencies: List[Dict], account_types: List[Dict]
):
    updated_accounts: Dict = st.session_state["edited_accounts_df"]["edited_rows"]
    if updated_accounts:
        for df_index, updated_account in updated_accounts.items():
            if updated_account.get("currency.name"):
                for currency in currencies:
                    if updated_account["currency.name"] == currency["name"]:
                        accounts[df_index]["currency_id"] = currency["id"]
            if updated_account.get("account_type.type"):
                for account_type in account_types:
                    if updated_account["account_type.type"] == account_type["type"]:
                        accounts[df_index]["account_type_id"] = account_type["id"]
            # api call to update accounts
            payload: Dict = {
                "name": updated_account.get("name", accounts[df_index]["name"]),
                "currency_id": accounts[df_index]["currency_id"],
                "account_type_id": accounts[df_index]["account_type_id"],
            }
            account_id = accounts[df_index]["id"]
            requests.patch(url=f"{API_URL}/accounts/{account_id}", json=payload)


def delete_accounts(accounts: List[Dict]):
    deleted_accounts: List = st.session_state["edited_accounts_df"]["deleted_rows"]
    if deleted_accounts:
        for deleted_account_index in deleted_accounts:
            account_id: str = accounts[deleted_account_index]["id"]
            # api call to delete account
            requests.delete(url=f"{API_URL}/accounts/{account_id}")


def main():
    set_up_page()
    get_accounts()
    # TODO: Add a form to create new accounts with a better UI
    # https://docs.streamlit.io/develop/concepts/architecture/forms
    # https://docs.streamlit.io/develop/api-reference/execution-flow/st.dialog


if __name__ == "__main__":
    main()
