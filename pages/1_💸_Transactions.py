import streamlit as st
import psycopg2
import pandas as pd
from datetime import date
from utils import (
    init_connection,
    run_query_list,
    run_query_pandas,
    categories
)


# TODO: Put this in a utils file
def set_up_page():
    page_title: str = "Wealth Tracker"
    page_icon: str = "💰"
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="centered",
        initial_sidebar_state="expanded",
    )
    st.title("Transactions")


def create_transaction(conn):
    col1, col2 = st.columns(2)

    assets_list: list = run_query_list(_conn=conn, query="SELECT ID, NAME FROM WEALTH_TRACKER.ASSET ORDER BY NAME DESC")
    asset_liability: str = col1.selectbox("Pick an asset/liability", assets_list)
    transaction_date: str = col2.date_input("Transaction date:")
    amount = col1.number_input("Amount (negative if it is an expense)")
    detail: str = col2.text_input("Detail:", placeholder="Burger King")
    category: str = col1.selectbox(
        "Pick a category:", key="category_selected", options=categories.keys()
    )
    # FIXME: https://docs.streamlit.io/library/api-reference/session-state#forms-and-callbacks
    subcategory: str = col2.selectbox("Pick a subcategory", categories[category])

    if st.form_submit_button("Submit"):
        st.write("A new transaction has been created")
        insert_transaction_dml: str = f"""
            INSERT INTO WEALTH_TRACKER.TRANSACTION (
                ID,
                ASSET_ID,
                DATE,
                AMOUNT,
                DETAIL,
                CATEGORY,
                SUBCATEGORY,
                CREATED_AT,
                UPDATED_AT
            ) VALUES (
                DEFAULT,
                {list(asset_liability)[0]},
                '{transaction_date}',
                {amount},
                '{detail}',
                '{category}',
                '{subcategory}',
                DEFAULT,
                DEFAULT
            )
            RETURNING ID
            ;
        """
        run_query_list(_conn=conn, query=insert_transaction_dml)
        update_balance_dml = f"UPDATE WEALTH_TRACKER.ASSET SET BALANCE = BALANCE + {amount} WHERE ID = {list(asset_liability)[0]} RETURNING ID"
        run_query_list(_conn=conn, query=update_balance_dml)


def main():
    set_up_page()

    # Connect to database
    conn: psycopg2.extensions.connection = init_connection()

    # Create a transaction
    with st.form("form"):
        st.subheader("Create a new transaction 👇")
        create_transaction(conn=conn)

    # List transactions
    st.subheader("Latest transactions 🤓")
    transactions_query = """
        SELECT *
        FROM WEALTH_TRACKER.TRANSACTION 
        ORDER BY DATE DESC
        """
    df: pd.DataFrame = run_query_pandas(_conn=conn, query=transactions_query)
    with st.form("form_edit_transactions"):
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            disabled=["created_at", "updated_at"],
            hide_index=True,
            column_config={
                "name": "Name",
                "category": st.column_config.SelectboxColumn("Category", options=categories.keys()),
                "created_at": "Created at",
                "updated_at": "Last updated at",
            },
            key='edited_df'
        )
        submitted = st.form_submit_button("Update transactions")
    if submitted:
        # TODO: Update, delete, add transactions
        st.write("Edited dataframe:", edited_df)
        st.write(st.session_state['edited_df'])



if __name__ == "__main__":
    main()
