import streamlit as st
import psycopg2
import pandas as pd
import numpy as np
from database import init_connection, run_query_list


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
    st.write("This is a summary of your networth ...")


def main():
    set_up_page()

    # Connect to database
    conn: psycopg2.extensions.connection = init_connection()

    st.header("💰 Total Net Worth")
    total_net_worth_query = "SELECT SUM(BALANCE) FROM WEALTH_TRACKER.ASSET"
    total_net_worth: str = run_query_list(_conn=conn, query=total_net_worth_query)[0][0]
    col1, col2 = st.columns(2)
    col1.metric(label="Net Worth", value=str(total_net_worth), delta=-5000000)
    chart_data = pd.DataFrame(
        np.random.randn(10, 1),
        columns=['a'])
    col2.area_chart(chart_data, height=200)


    st.header("📈 Assets")
    balance_per_asset_query: str = "SELECT NAME, CURRENCY, SUM(BALANCE) FROM WEALTH_TRACKER.ASSET GROUP BY NAME, CURRENCY"
    balance_per_asset: str = run_query_list(_conn=conn, query=balance_per_asset_query)
    for asset in balance_per_asset:
        col1, col2 = st.columns(2)
        col1.metric(label=asset[0], value=f"{asset[1]} {str(asset[2])}",  delta="1.000.000")
        chart_data = pd.DataFrame(
            np.random.randn(10, 1),
            columns=['a'])
        col2.area_chart(chart_data, height=200)

    st.header("📉 Liabilities")

    st.header("📊 Upcoming Transactions")



if __name__ == "__main__":
    main()