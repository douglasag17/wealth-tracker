import streamlit as st
import psycopg2
import pandas.io.sql as sqlio
import pandas as pd
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


asset_types: tuple = (
    "Cash",
    "Saving Account",
    "Checking Account",
    "Investment",
    "Real Estate",
    "Vehicle",
    "Other",
)

currencies: tuple = ("USD", "COP")

categories = {
    "income": ("wage", "gift"),
    "housing": ("rent", "internet"),
    "vehicle": ("fuel", "parking"),
}


# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection() -> psycopg2.extensions.connection:
    return psycopg2.connect(**st.secrets["postgres"])


# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)
def run_query_list(_conn: psycopg2.extensions.connection, query: str) -> list:
    with _conn.cursor() as cur:
        cur.execute(query)
        _conn.commit()
        return cur.fetchall()


# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)
def run_query_pandas(_conn: psycopg2.extensions.connection, query: str) -> pd.DataFrame:
    return sqlio.read_sql_query(query, _conn)


def login() -> bool:
    # Log In Page
    with open("config.yaml") as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
        config["preauthorized"],
    )
    name, authentication_status, username = authenticator.login("Login", "sidebar")
    if st.session_state["authentication_status"]:
        authenticator.logout("Logout", "sidebar")
        # st.sidebar.write(f"Welcome *{name}*")
        return True
    elif st.session_state["authentication_status"] is None:
        st.sidebar.warning("Please enter your username and password")
        return False
    elif not st.session_state["authentication_status"]:
        st.sidebar.error("Username/password is incorrect")
        return False
