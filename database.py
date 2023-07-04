import streamlit as st
import psycopg2
import pandas.io.sql as sqlio
import pandas as pd


# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection() -> psycopg2.extensions.connection:
    return psycopg2.connect(**st.secrets["postgres"])


# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query_list(_conn: psycopg2.extensions.connection, query: str) -> list:
    with _conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query_pandas(_conn: psycopg2.extensions.connection, query: str) -> pd.DataFrame:
    return sqlio.read_sql_query(query, _conn)
