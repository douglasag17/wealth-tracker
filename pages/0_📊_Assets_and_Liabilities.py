import streamlit as st
import psycopg2
import pandas as pd
from utils import (
    init_connection,
    run_query_list,
    run_query_pandas,
    asset_types,
    currencies,
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
    st.title("Assets and Liabilities")
    st.write("These are your assets and liabilities ...")


def create_asset(conn):
    col1, col2 = st.columns(2)
    name: str = col1.text_input("Name:", placeholder="Saving Account Bancolombia")
    asset_type: str = col2.selectbox("Type", asset_types)
    information: str = col1.text_input(
        "Information:", placeholder="Account Number, Address, Car Model, etc"
    )
    currency: str = col2.selectbox("Currency", currencies)
    balance = col1.number_input("Initial balance")
    if st.form_submit_button("Complete"):
        st.write("Your responses were saved")
        dml: str = f"""
            INSERT INTO WEALTH_TRACKER.ASSET (
                ID,
                NAME,
                TYPE,
                INFORMATION,
                CURRENCY,
                BALANCE,
                IS_ACTIVE,
                CREATED_AT,
                UPDATED_AT
            ) VALUES (
                DEFAULT,
                '{name}',
                '{asset_type}',
                '{information}',
                '{currency}',
                {balance},
                DEFAULT,
                DEFAULT,
                DEFAULT
            )
            RETURNING ID
            ;
        """
        run_query_list(_conn=conn, query=dml)


def list_assets(conn):
    assets_query: str = "SELECT * FROM WEALTH_TRACKER.ASSET ORDER BY CREATED_AT DESC"
    assets: str = run_query_list(_conn=conn, query=assets_query)
    for i, asset in enumerate(assets):
        with st.form(f"asset_form_{i}"):
            col1, col2 = st.columns(2)
            name: str = col1.text_input("Name:", asset[1])
            asset_type: str = col2.selectbox(
                "Type", asset_types, index=asset_types.index(asset[2])
            )
            information: str = col1.text_input(
                "Information:",
                asset[3],
                placeholder="Account Number, Address, Car Model, etc",
            )
            currency: str = col2.selectbox(
                "Currency", currencies, index=currencies.index(asset[4])
            )
            col1.number_input("Current balance", float(asset[5]), disabled=True)
            col2.date_input("Created at", asset[7], disabled=True)
            col1.date_input("Last updated at", asset[8], disabled=True)
            col1, col2, col3 = st.columns(3)
            is_active: bool = col3.checkbox("Is it active?", asset[6])
            if col1.form_submit_button("Update"):
                update_query = f"""
                    UPDATE WEALTH_TRACKER.ASSET 
                    SET NAME = '{name}',
                        TYPE = '{asset_type}',
                        INFORMATION = '{information}',
                        CURRENCY = '{currency}',
                        IS_ACTIVE = {is_active},
                        UPDATED_AT = LOCALTIMESTAMP
                    WHERE ID = {asset[0]}
                    RETURNING ID;
                    """
                run_query_list(_conn=conn, query=update_query)
            if col2.form_submit_button("Delete"):
                delete_query = f"DELETE FROM WEALTH_TRACKER.ASSET WHERE ID = {asset[0]} RETURNING ID;"
                run_query_list(_conn=conn, query=delete_query)


def main():
    set_up_page()

    # Connect to database
    conn: psycopg2.extensions.connection = init_connection()

    # Create an asset or a liability
    with st.form("form"):
        st.subheader("Create a new asset 👇")
        create_asset(conn=conn)

    # List assets
    st.header("📈 Assets")
    list_assets(conn=conn)


    # TODO: Use a table instead of a single form
    # assets_query = "SELECT NAME, TYPE, INFORMATION, CURRENCY, BALANCE, IS_ACTIVE, CREATED_AT, UPDATED_AT FROM WEALTH_TRACKER.ASSET"
    # df: pd.DataFrame = run_query_pandas(_conn=conn, query=assets_query)
    # edited_df: pd.DataFrame = st.data_editor(
    #     df,
    #     column_config={
    #         "name": "Name",
    #         "type": st.column_config.SelectboxColumn("Type", options=asset_types),
    #         "information": "Information",
    #         "currency": st.column_config.SelectboxColumn(
    #             "Currency", options=currencies
    #         ),
    #         "balance": "Balance",
    #         "is_active": "Is it active?",
    #         "created_at": "Created at",
    #         "updated_at": "Last updated at",
    #     },
    #     disabled=["balance", "created_at", "updated_at"],
    #     hide_index=True,
    #     num_rows="dynamic"
    # )

    # List liabilities
    st.header("📈 Liabilities")


if __name__ == "__main__":
    main()
