import streamlit as st
import psycopg2
import pandas as pd
from utils import init_connection, run_query_list, run_query_pandas


if __name__ == "__main__":
    page_title: str = "Survey App"
    page_icon: str = "👀"
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="centered",
        initial_sidebar_state="expanded",
    )
    st.title(f"{page_icon} {page_title}")

    # Connect to database
    conn: psycopg2.extensions.connection = init_connection()

    st.header("📊 Survey Results")

    st.subheader("Respondents")
    respondents_query = "SELECT * FROM SURVEY_RESPONDENTS ORDER BY CREATED_AT DESC;"
    st.dataframe(run_query_pandas(_conn=conn, query=respondents_query))

    st.subheader("Responses")
    responses_query = "SELECT * FROM SURVEY_RESPONSES ORDER BY CREATED_AT DESC;"
    st.dataframe(run_query_pandas(_conn=conn, query=responses_query))
