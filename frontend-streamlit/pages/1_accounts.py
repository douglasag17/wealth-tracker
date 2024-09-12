import streamlit as st
import requests
import pandas as pd
from typing import List, Dict
from utils import (
    set_up_page,
    get_data_from_api,
    get_dataframes,
    API_URL,
)


def get_accounts(api_data: Dict[str, List[Dict]], dataframes: Dict[str, pd.DataFrame]):
    st.subheader("Accounts")

    # Getting data
    accounts: List[Dict] = api_data["accounts"]
    currencies: List[Dict] = api_data["currencies"]
    account_types: List[Dict] = api_data["account_types"]
    accounts_df: pd.DataFrame = dataframes["accounts_df"]

    # Get total balance by summing all the balances from accounts_df
    total_balance: float = accounts_df["balance_cop"].sum()
    total_balance_formatted: str = f"${total_balance:,.0f}"

    # Adding Metrics
    col1, col2 = st.columns(2)
    # TODO: Gettting delta value for total balance metric card to show if it increased or decreased from the previous period
    col1.metric(
        "Total Balance",
        value=total_balance_formatted,
        # delta=0,
        # delta_color="inverse",
        help="Shows the total balance of all accounts",
    )
    col2.metric("Total Credit", "9 mph", "-8%")

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
    disabled: List = ["created_at", "updated_at", "balance"]

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
                    new_account["currency_id"] = currency["id"]
            for account_type in account_types:
                if new_account["account_type.type"] == account_type["type"]:
                    new_account["account_type_id"] = account_type["id"]
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

    # Getting data from API
    api_data: Dict[str, List[Dict]] = get_data_from_api()
    dataframes: Dict[str, pd.DataFrame] = get_dataframes(api_data)

    # Get accounts data_editor form
    get_accounts(api_data=api_data, dataframes=dataframes)

    # TODO: Add a form to create new accounts with a better UI
    # https://docs.streamlit.io/develop/concepts/architecture/forms
    # https://docs.streamlit.io/develop/api-reference/execution-flow/st.dialog


if __name__ == "__main__":
    main()
