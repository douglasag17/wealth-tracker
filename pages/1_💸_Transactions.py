import streamlit as st
import psycopg2
import pandas as pd
from datetime import date
from utils import init_connection, run_query_list, run_query_pandas, categories, login


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


def create_transaction(conn: psycopg2.extensions.connection, assets_list: list):
    # Create a transaction
    with st.form("form"):
        st.subheader("Create a new transaction 👇")
        col1, col2 = st.columns(2)
        asset_liability: str = col1.selectbox("Pick an asset/liability", assets_list)
        transaction_date: str = col2.date_input("Transaction date:")
        amount = col1.number_input("Amount (negative if it is an expense)")
        detail: str = col2.text_input("Detail:", placeholder="Burger King")
        category: str = col1.selectbox(
            "Pick a category:", key="category_selected", options=categories
        )
        # FIXME: https://docs.streamlit.io/library/api-reference/session-state#forms-and-callbacks
        # Try session state https://docs.streamlit.io/library/api-reference/session-state
        # subcategory: str = col2.selectbox("Pick a subcategory", categories[category])

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
                    CREATED_AT,
                    UPDATED_AT
                ) VALUES (
                    DEFAULT,
                    {list(asset_liability)[0]},
                    '{transaction_date}',
                    {amount},
                    '{detail}',
                    '{category}',
                    DEFAULT,
                    DEFAULT
                )
                RETURNING ID
                ;
            """
            run_query_list(_conn=conn, query=insert_transaction_dml)


def show_transactions(conn: psycopg2.extensions.connection, assets_list: list):
    # List transactions
    st.subheader("Latest transactions 🤓")
    transactions_query: str = """
        SELECT 
            T.ID AS TRANSACTION_ID,
            T.ASSET_ID,
            CAST(T.ASSET_ID AS VARCHAR) || ',' || A.NAME AS ASSET_NAME,
            T.DATE,
            T.AMOUNT,
            T.DETAIL,
            T.CATEGORY,
            T.CREATED_AT,
            T.UPDATED_AT
        FROM WEALTH_TRACKER.TRANSACTION T
        JOIN WEALTH_TRACKER.ASSET A
            ON T.ASSET_ID = A.ID
        ORDER BY T.UPDATED_AT DESC
        """
    df: pd.DataFrame = run_query_pandas(_conn=conn, query=transactions_query)
    with st.form("form_edit_transactions"):
        edited_df: pd.DataFrame = st.data_editor(
            df,
            num_rows="dynamic",
            disabled=["transaction_id", "created_at", "updated_at"],
            column_order=(
                "asset_name",
                "amount",
                "category",
                "date",
                "detail",
                "updated_at",
            ),
            key="edited_df",
            column_config={
                "transaction_id": "Transaction ID",
                "asset_name": st.column_config.SelectboxColumn(
                    "Asset Name", options=assets_list
                ),
                "date": "Transaction Date",
                "amount": "Amount (negative for expenses)",
                "detail": "Detail",
                "category": st.column_config.SelectboxColumn(
                    "Category", options=categories
                ),
                "created_at": "Created at",
                "updated_at": "Last updated at",
            },
        )
        if st.form_submit_button("Update transactions"):
            cdc_df: dict = st.session_state["edited_df"]
            st.write(cdc_df)
            if cdc_df["deleted_rows"]:
                for index in cdc_df["deleted_rows"]:
                    row_to_delete: pd.Series = df.iloc[index]
                    delete_transaction_dml: str = f"DELETE FROM WEALTH_TRACKER.TRANSACTION WHERE ID = {row_to_delete['transaction_id']} RETURNING ID"
                    run_query_list(_conn=conn, query=delete_transaction_dml)
            if cdc_df["edited_rows"]:
                for index, column in cdc_df["edited_rows"].items():
                    row_to_update: pd.Series = df.iloc[index]
                    update_transaction_dml: str = f"""
                        UPDATE WEALTH_TRACKER.TRANSACTION 
                        SET ASSET_ID = {column.get('asset_id', row_to_update['asset_id'])},
                            DATE = '{column.get('date', row_to_update['date'])}',
                            AMOUNT = {column.get('amount', row_to_update['amount'])},
                            DETAIL = '{column.get('detail', row_to_update['detail'])}',
                            CATEGORY = '{column.get('category', row_to_update['category'])}',
                            UPDATED_AT = LOCALTIMESTAMP
                        WHERE ID = {row_to_update['transaction_id']}
                        RETURNING ID;
                        """
                    run_query_list(_conn=conn, query=update_transaction_dml)


def main():
    set_up_page()

    # Connect to database
    conn: psycopg2.extensions.connection = init_connection()
    assets_list: list = run_query_list(
        _conn=conn, query="SELECT ID, NAME FROM WEALTH_TRACKER.ASSET ORDER BY NAME DESC"
    )

    if login():
        create_transaction(
            conn=conn, assets_list=assets_list
        )  # FIXME: Transactions are being duplicated because of login
        show_transactions(conn=conn, assets_list=assets_list)
    else:
        st.warning("Please enter your username and password")


if __name__ == "__main__":
    main()
