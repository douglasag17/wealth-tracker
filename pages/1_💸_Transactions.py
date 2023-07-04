import streamlit as st
import psycopg2
import pandas as pd
from database import init_connection, run_query_list, run_query_pandas


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
    st.title("Assets and Liabilities")
    st.write("This is a summary of your assets and liabilities ...")


def main():
    set_up_page()

    # Connect to database
    conn: psycopg2.extensions.connection = init_connection()

    # List assets and liabilities 
    types: tuple = ('Cash', 'Saving Account', 'Checking Account', 'Investment', 'Real Estate', 'Vehicle', 'Other')
    currencies: tuple = ('USD', 'COP')
    assets_query = "SELECT NAME, TYPE, INFORMATION, CURRENCY, BALANCE, IS_ACTIVE, CREATED_AT, UPDATED_AT FROM WEALTH_TRACKER.ASSET"
    df: pd.DataFrame = run_query_pandas(_conn=conn, query=assets_query)
    edited_df: pd.DataFrame = st.data_editor(
        df,
        column_config={
            "name": "Name",
            "type": st.column_config.SelectboxColumn(
                "Type",
                options=types
            ),
            "information": "Information",
            "currency": st.column_config.SelectboxColumn(
                "Currency",
                options=currencies
            ),
            "balance": "Balance",
            "is_active": "Is it active?",
            "created_at": "Created at",
            "updated_at": "Lasta updated"
        },
        disabled=["balance", "created_at", "updated_at"],
        hide_index=True
    )
    # TODO: Update assets

if __name__ == "__main__":
    main()
