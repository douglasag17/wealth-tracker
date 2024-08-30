import streamlit as st
import requests
from utils import set_up_page, API_URL
import pandas as pd
from typing import List, Dict


def get_accounts():
    st.subheader("Accounts")

    # Getting data from API
    accounts: List[Dict] = requests.get(url=f"{API_URL}/accounts/").json()
    currencies: List[Dict] = requests.get(url=f"{API_URL}/currencies/").json()
    account_types: List[Dict] = requests.get(url=f"{API_URL}/account_types/").json()

    # Creating Dataframe
    accounts_df = pd.json_normalize(accounts)

    # Writing table
    column_config: Dict = {
        "name": st.column_config.TextColumn("Name", required=True),
        "currency.name": st.column_config.SelectboxColumn(
            "Currency",
            required=True,
            options=[currency["name"] for currency in currencies],
        ),
        "account_type.type": st.column_config.SelectboxColumn(
            "Type",
            required=True,
            options=[account_type["type"] for account_type in account_types],
        ),
        "created_at": st.column_config.DatetimeColumn(
            "Created At", format="YYYY-MM-DD HH:mm:ss"
        ),
        "updated_at": st.column_config.DatetimeColumn(
            "Updated At", format="YYYY-MM-DD HH:mm:ss"
        ),
    }
    column_order = ("name", "currency.name", "account_type.type")
    disabled: list = ["created_at", "updated_at"]

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
            # Insert new accounts
            added_accounts: List[Dict] = st.session_state["edited_accounts_df"][
                "added_rows"
            ]
            if added_accounts:
                # Adding foreing keys
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

            # Update accounts
            updated_accounts: Dict = st.session_state["edited_accounts_df"][
                "edited_rows"
            ]
            if updated_accounts:
                # Adding foreing keys
                for df_index, updated_account in updated_accounts.items():
                    if updated_account.get("currency.name"):
                        for currency in currencies:
                            if updated_account["currency.name"] == currency["name"]:
                                accounts[df_index]["currency_id"] = currency["id"]
                    if updated_account.get("account_type.type"):
                        for account_type in account_types:
                            if (
                                updated_account["account_type.type"]
                                == account_type["type"]
                            ):
                                accounts[df_index]["account_type_id"] = account_type[
                                    "id"
                                ]
                    # api call to update accounts
                    payload: Dict = {
                        "name": updated_account.get("name", accounts[df_index]["name"]),
                        "currency_id": accounts[df_index]["currency_id"],
                        "account_type_id": accounts[df_index]["account_type_id"],
                    }
                    account_id = accounts[df_index]["id"]
                    requests.patch(url=f"{API_URL}/accounts/{account_id}", json=payload)

            # Delete accounts
            deleted_accounts: list = st.session_state["edited_accounts_df"][
                "deleted_rows"
            ]
            if deleted_accounts:
                # Getting primary key
                for deleted_account_index in deleted_accounts:
                    account_id = accounts[deleted_account_index]["id"]
                    # api call to delete account
                    requests.delete(url=f"{API_URL}/accounts/{account_id}")

            # Refresh app
            st.rerun()


def main():
    set_up_page()
    get_accounts()
    # TODO: Add a form to create new accounts with a better UI
    # https://docs.streamlit.io/develop/concepts/architecture/forms
    # https://docs.streamlit.io/develop/api-reference/execution-flow/st.dialog


if __name__ == "__main__":
    main()
