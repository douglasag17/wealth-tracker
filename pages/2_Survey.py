import streamlit as st
import psycopg2
import pandas as pd
from database import init_connection, run_query_list, run_query_pandas


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

    st.header("📊 Survey")
    st.write("A Survey Web App created with the purpose of testing out this project https://github.com/douglasag17/real-time-data-to-snowflake")
    st.write("Alternative: https://c4nmnzwd34e7byeayqqhqij6su0klfiq.lambda-url.us-east-1.on.aws/")
    st.subheader("Fill out the survey")

    with st.container():
        st.radio(
            "I consider myself: 👇",
            ["Extroverted", "Introverted"],
            key="q1",
        )
        st.session_state.q1

    with st.container():
        if st.button('Complete'):
            st.write('Your responses were saved')
