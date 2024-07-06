import streamlit as st
import requests
from utils import set_up_page, API_URL


def get_accounts():
    st.subheader("Accounts")

    # Getting data from API
    accounts: list[dict] = requests.get(url=f"{API_URL}/accounts/").json()
    currencies: list[dict] = requests.get(url=f"{API_URL}/currencies/").json()
    account_types: list[dict] = requests.get(url=f"{API_URL}/account_types/").json()

    # Joining values from foreign keys
    for i, account in enumerate(accounts):
        for currency in currencies:
            if account["currency_id"] == currency["id"]:
                accounts[i]["currency"] = currency["name"]
        for account_type in account_types:
            if account["account_type_id"] == account_type["id"]:
                accounts[i]["account_type"] = account_type["type"]

    # Writing table
    column_config: str = {
        "name": st.column_config.TextColumn("Name", required=True),
        "currency": st.column_config.SelectboxColumn(
            "Currency", required=True, options=[currency["name"] for currency in currencies]
        ),
        "account_type": st.column_config.SelectboxColumn(
            "Type", required=True, options=[account_type["type"] for account_type in account_types]
        ),
    }
    column_order = ("name", "currency", "account_type")

    with st.form("form_edit_accounts"):
        edited_accounts = st.data_editor(
            accounts,
            key="edited_accounts",
            num_rows="dynamic",
            column_config=column_config,
            column_order=column_order,
            hide_index=True
        )

        # Updated data
        # st.write("edited_accounts")
        # st.write(edited_accounts)
        st.write("added_rows")
        st.write(st.session_state["edited_accounts"]["added_rows"])
        st.write("edited_rows")
        st.write(st.session_state["edited_accounts"]["edited_rows"])
        st.write("deleted_rows")
        st.write(st.session_state["edited_accounts"]["deleted_rows"])

        # Submit button
        if st.form_submit_button("Update accounts"):
            
            # Insert new accounts
            added_accounts: list[dict] = st.session_state["edited_accounts"]["added_rows"]
            if added_accounts:
                # Adding foreing keys
                for i, new_account in enumerate(added_accounts):
                    for currency in currencies:
                        if new_account["currency"] == currency["name"]:
                            added_accounts[i]["currency_id"] = currency["id"]
                    for account_type in account_types:
                        if new_account["account_type"] == account_type["type"]:
                            added_accounts[i]["account_type_id"] = account_type["id"]
                    
                    payload: dict = {
                        "name": new_account["name"],
                        "account_type_id": new_account["account_type_id"],
                        "currency_id": new_account["currency_id"]
                    }
                    # api call to add new accounts
                    requests.post(url=f"{API_URL}/accounts/", json=payload)
            
            # Update accounts
            updated_accounts: dict = st.session_state["edited_accounts"]["edited_rows"]
            if updated_accounts:
                pass

            # Delete accounts
            deleted_accounts: list = st.session_state["edited_accounts"]["deleted_rows"]
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


if __name__ == "__main__":
    main()
