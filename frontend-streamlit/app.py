import streamlit as st
import requests


API_URL: str = "http://127.0.0.1:8000"


def set_up_page():
    page_title: str = "Wealth Tracker"
    page_icon: str = "💰"
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="centered",
        initial_sidebar_state="expanded",
    )
    st.title(f"{page_icon} {page_title}")


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
        "name": st.column_config.TextColumn("Name", width="large", required=True),
        "currency": st.column_config.SelectboxColumn(
            "Currency", options=[currency["name"] for currency in currencies]
        ),
        "account_type": st.column_config.SelectboxColumn(
            "Type", options=[account_type["type"] for account_type in account_types]
        ),
    }
    column_order = ("name", "currency", "account_type")
    edited_accounts = st.data_editor(
        accounts,
        key="edited_accounts",
        num_rows="dynamic",
        column_config=column_config,
        column_order=column_order,
        hide_index=True
    )

    # Updated data
    st.write("edited_rows")
    st.write(st.session_state["edited_accounts"]["edited_rows"])
    st.write("added_rows")
    st.write(st.session_state["edited_accounts"]["added_rows"])
    st.write("deleted_rows")
    st.write(st.session_state["edited_accounts"]["deleted_rows"])

    if st.button("Update accounts"):
        # Insert new accounts
        if st.session_state["edited_accounts"]["added_rows"]:
            pass
        
        # Update accounts
        if st.session_state["edited_accounts"]["edited_rows"]:
            pass

        # Delete accounts
        if st.session_state["edited_accounts"]["deleted_rows"]:
            pass
        
        # Refresh app
        st.rerun()

def main():
    set_up_page()
    get_accounts()


if __name__ == "__main__":
    main()
