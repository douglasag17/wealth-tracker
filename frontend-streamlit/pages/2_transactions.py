import streamlit as st
import requests
from utils import set_up_page, API_URL
import pandas as pd
from typing import List, Dict
from datetime import datetime, date


def get_transactions():
    st.subheader("Transactions")

    # Getting data from API
    # FIXME: Add support for filtering by date to API
    transactions: List[Dict] = requests.get(url=f"{API_URL}/transactions/").json()
    accounts: List[Dict] = requests.get(url=f"{API_URL}/accounts/").json()
    categories: List[Dict] = requests.get(url=f"{API_URL}/categories/").json()
    subcategories: List[Dict] = requests.get(url=f"{API_URL}/sub_categories/").json()

    # Creating Dataframe
    transactions_df: pd.DataFrame = pd.json_normalize(transactions)

    transactions_df["transaction_date"] = pd.to_datetime(
        transactions_df["transaction_date"]
    )

    # Filtering data to show only the transactions within the date range selected
    date_range_filter: List[date] = st.session_state["date_range_filter"]
    if len(date_range_filter) == 2:
        start_date: date = date_range_filter[0]
        end_date: date = date_range_filter[1]
        transactions_df = transactions_df[
            (
                transactions_df["transaction_date"]
                >= datetime.combine(start_date, datetime.min.time())
            )
            & (
                transactions_df["transaction_date"]
                <= datetime.combine(end_date, datetime.max.time())
            )
        ]

    # Adding a column with the category and subcategory, this relates to the selectbox
    transactions_df["categories_with_subcategories"] = (
        transactions_df["category.name"] + " - " + transactions_df["subcategory.name"]
    )

    # Ordering rows in the dataframe
    # transactions_df.sort_values(
    #     by=["transaction_date"], inplace=True, ignore_index=True, ascending=False
    # )

    # Writing table
    column_config: Dict = {
        "transaction_date": st.column_config.DatetimeColumn(
            "Transaction Date",
            format="YYYY-MM-DD HH:mm:ss.SSS",
            required=True,
            help="Select the date and time of the transaction",
            # FIXME: this is not working, it refreshes st.session_state
            # default=datetime.now(timezone.utc),
        ),
        "account.name": st.column_config.SelectboxColumn(
            "Account",
            required=True,
            help="Select the account where the transaction belongs",
            options=[account["name"] for account in accounts],
        ),
        "amount": st.column_config.NumberColumn(
            "Amount",
            required=True,
            help="Add the amount of the transaction. Currency depends on the selected account",
        ),
        "categories_with_subcategories": st.column_config.SelectboxColumn(
            "Category",
            required=True,
            help="Select the category and subcategory of the transaction",
            options=[
                f"{subcategory["category"]["name"]} - {subcategory["name"]}"
                for subcategory in subcategories
            ],
        ),
        "description": st.column_config.TextColumn(
            "Description", help="Optional - Add a description to the transaction"
        ),
    }
    column_order = (
        "transaction_date",
        "account.name",
        "amount",
        "categories_with_subcategories",
        "description",
    )
    disabled: list = ["created_at", "updated_at"]

    with st.form("form_edit_transactions"):
        st.data_editor(
            transactions_df,
            key="edited_transactions_df",
            column_config=column_config,
            column_order=column_order,
            disabled=disabled,
            use_container_width=True,
            hide_index=False,
            num_rows="dynamic",
        )

        # Submit button
        if st.form_submit_button("Save changes"):
            st.write(st.session_state)
            delete_transactions(transactions)
            insert_new_transactions(accounts, categories, subcategories)
            update_transactions(transactions, accounts, categories, subcategories)

            # Refresh app
            st.rerun()


def delete_transactions(transactions: List[Dict]):
    deleted_transactions: List = st.session_state["edited_transactions_df"][
        "deleted_rows"
    ]
    if deleted_transactions:
        for deleted_transaction_index in deleted_transactions:
            transaction_id: str = transactions[deleted_transaction_index]["id"]

            # api call to delete account
            requests.delete(url=f"{API_URL}/transactions/{transaction_id}")


def insert_new_transactions(
    accounts: List[Dict], categories: List[Dict], subcategories: List[Dict]
):
    added_transactions: List[Dict] = st.session_state["edited_transactions_df"][
        "added_rows"
    ]
    if added_transactions:
        for i, new_transaction in enumerate(added_transactions):
            new_category: str = new_transaction["categories_with_subcategories"].split(
                " - "
            )[0]
            new_subcategory: str = new_transaction[
                "categories_with_subcategories"
            ].split(" - ")[1]
            for account in accounts:
                if new_transaction["account.name"] == account["name"]:
                    new_transaction["account_id"] = account["id"]
            for category in categories:
                if new_category == category["name"]:
                    new_transaction["category_id"] = category["id"]

            for subcategory in subcategories:
                if new_subcategory == subcategory["name"]:
                    new_transaction["subcategory_id"] = subcategory["id"]

            # api call to add new transactions
            st.write(new_transaction["transaction_date"])
            new_transaction_date: datetime = datetime.strptime(
                new_transaction["transaction_date"], "%Y-%m-%dT%H:%M:%S.%f"
            )
            payload: Dict = {
                "transaction_date": new_transaction_date.strftime(
                    "%Y-%m-%dT%H:%M:%S.%f"
                ),
                "account_id": new_transaction["account_id"],
                "amount": new_transaction["amount"],
                "category_id": new_transaction["category_id"],
                "subcategory_id": new_transaction["subcategory_id"],
                "description": new_transaction.get("description", ""),
            }
            requests.post(url=f"{API_URL}/transactions/", json=payload)


def update_transactions(
    transactions: List[Dict],
    accounts: List[Dict],
    categories: List[Dict],
    subcategories: List[Dict],
):
    updated_transactions: Dict = st.session_state["edited_transactions_df"][
        "edited_rows"
    ]
    if updated_transactions:
        for df_index, updated_transaction in updated_transactions.items():
            if updated_transaction.get("account.name"):
                for account in accounts:
                    if updated_transaction["account.name"] == account["name"]:
                        transactions[df_index]["account_id"] = account["id"]
            if updated_transaction.get("categories_with_subcategories"):
                updated_category: str = updated_transaction[
                    "categories_with_subcategories"
                ].split(" - ")[0]
                updated_subcategory: str = updated_transaction[
                    "categories_with_subcategories"
                ].split(" - ")[1]
                for category in categories:
                    if updated_category == category["name"]:
                        transactions[df_index]["category_id"] = category["id"]
                for subcategory in subcategories:
                    if updated_subcategory == subcategory["name"]:
                        transactions[df_index]["subcategory_id"] = subcategory["id"]
            if updated_transaction.get("transaction_date"):
                updated_transaction_date: datetime = datetime.strptime(
                    updated_transaction["transaction_date"], "%Y-%m-%dT%H:%M:%S.%f"
                )
                transactions[df_index]["transaction_date"] = (
                    updated_transaction_date.strftime("%Y-%m-%dT%H:%M:%S.%f")
                )

            # api call to update transactions
            payload: Dict = {
                "transaction_date": transactions[df_index]["transaction_date"],
                "account_id": transactions[df_index]["account_id"],
                "amount": updated_transaction.get(
                    "amount", transactions[df_index]["amount"]
                ),
                "category_id": transactions[df_index]["category_id"],
                "subcategory_id": transactions[df_index]["subcategory_id"],
                "description": updated_transaction.get(
                    "description", transactions[df_index]["description"]
                ),
            }
            transaction_id = transactions[df_index]["id"]
            st.write(payload, transaction_id)
            response = requests.patch(
                url=f"{API_URL}/transactions/{transaction_id}", json=payload
            )
            st.write(response)


def main():
    set_up_page()
    # add form to add a transaction
    get_transactions()
    # TODO: Add a form to create new accounts with a better UI
    # https://docs.streamlit.io/develop/concepts/architecture/forms
    # https://docs.streamlit.io/develop/api-reference/execution-flow/st.dialog


if __name__ == "__main__":
    main()
