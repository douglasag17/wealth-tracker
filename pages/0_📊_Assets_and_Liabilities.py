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
    st.write("These are your assets and liabilities ...")


def main():
    set_up_page()

    # Connect to database
    conn: psycopg2.extensions.connection = init_connection()

    # List assets and liabilities 
    assets_query: str = "SELECT * FROM WEALTH_TRACKER.ASSET"
    assets: str = run_query_list(_conn=conn, query=assets_query)
    for i, asset in enumerate(assets):
        with st.form(f"asset_form_{i}"):
            st.write(asset)
            col1, col2 = st.columns(2)
            if submitted := col1.form_submit_button("Update"):
                pass
            if submitted := col2.form_submit_button("Delete"):
                pass
    
    # Create an asset or a liability
    with st.expander("Create a new asset"):
        with st.form("form"):
            name: str = st.text_input("Name:", placeholder="Saving Account Bancolombia")
            types: tuple = ('Cash', 'Saving Account', 'Checking Account', 'Investment', 'Real Estate', 'Vehicle', 'Other')
            asset_type: str = st.selectbox('Type', types)
            information: str = st.text_input("Information:", placeholder="Account Number, Address, Car Model, etc")
            currencies: tuple = ('USD', 'COP')
            currency: str = st.selectbox('Currency', currencies)
            balance = st.number_input('Initial balance')

            if submitted := st.form_submit_button("Complete"):
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
                conn.commit()

if __name__ == "__main__":
    main()
