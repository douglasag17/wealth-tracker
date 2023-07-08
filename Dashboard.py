import streamlit as st
import psycopg2
import pandas as pd
import numpy as np
from utils import init_connection, run_query_list, login


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
    st.title(f"{page_icon} {page_title}")


def show_dashboard(conn: psycopg2.extensions.connection):
    # Show dashboard
    st.write("This is a summary of your networth ...")
    # TODO: Add total liabilities
    st.header("💰 Total Net Worth")
    total_net_worth_query: str = """
        SELECT
            SUM(COALESCE(T.AMOUNT, A.BALANCE)) AS BALANCE
        FROM WEALTH_TRACKER.ASSET A
        LEFT JOIN WEALTH_TRACKER.TRANSACTION T
            ON A.ID = T.ASSET_ID
        """
    total_net_worth: str = run_query_list(_conn=conn, query=total_net_worth_query)[0][0]
    col1, col2 = st.columns(2)
    col1.metric(label="Total Net Worth", value=str(total_net_worth), delta=-5000000)
    chart_data = pd.DataFrame(np.random.randn(10, 1), columns=["a"])
    col2.area_chart(chart_data, height=200)

    st.header("📈 Assets")
    balance_per_asset_query: str = """
        SELECT
            A.NAME,
            A.CURRENCY,
            SUM(COALESCE(T.AMOUNT, A.BALANCE)) AS BALANCE
        FROM WEALTH_TRACKER.ASSET A
        LEFT JOIN WEALTH_TRACKER.TRANSACTION T
            ON A.ID = T.ASSET_ID
        GROUP BY 
            A.NAME,
            A.CURRENCY
        ORDER BY BALANCE DESC
        """

    balance_per_asset: str = run_query_list(_conn=conn, query=balance_per_asset_query)
    for asset in balance_per_asset:
        col1, col2 = st.columns(2)
        col1.metric(
            label=asset[0], value=f"{asset[1]} {str(asset[2])}", delta="1.000.000"
        )
        chart_data = pd.DataFrame(np.random.randn(10, 1), columns=["a"])
        col2.area_chart(chart_data, height=200)

    st.header("📉 Liabilities")

    st.header("📊 Upcoming Transactions")

    st.header("📊 Budget Summary")


def main():
    set_up_page()

    # Connect to database
    conn: psycopg2.extensions.connection = init_connection()

    if login():
        show_dashboard(conn)
    else:
        st.warning("Please enter your username and password")


if __name__ == "__main__":
    main()
