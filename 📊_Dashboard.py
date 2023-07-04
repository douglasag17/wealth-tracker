import streamlit as st
import psycopg2
import pandas as pd
from database import init_connection, run_query_list, run_query_pandas


if __name__ == "__main__":
    page_title: str = "Wealth Tracker"
    page_icon: str = "💰"
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="centered",
        initial_sidebar_state="expanded",
    )
    st.title(f"{page_icon} {page_title}")
    st.write(
        "aflksjgañsljfhñalskfh ñaslkfhañslk fhñalsjf ñlaskhfñ aslhkf ñaskasñlfk asñlfk "
    )

    # Connect to database
    conn: psycopg2.extensions.connection = init_connection()

    st.header("📊 Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Account1", value="$50.000.000", delta="$1.000.000")
    col2.metric(label="Ford Fiesta", value="$45.000.000", delta="-5.000.000")
    col3.metric(label="House", value="$500.000.000")

    query = "SELECT * FROM SURVEY_RESPONDENTS ORDER BY CREATED_AT DESC;"
    st.dataframe(run_query_pandas(_conn=conn, query=query))
