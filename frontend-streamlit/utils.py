import streamlit as st
from datetime import date, timedelta


API_URL: str = "http://127.0.0.1:8000"


def set_up_page():
    page_title: str = "Wealth Tracker"
    page_icon: str = "💰"
    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title(f"{page_icon} {page_title}")
    set_up_sidebar()


def set_up_sidebar():
    # Date range filter
    today = date.today()
    first_day_of_month = date(today.year, today.month, 1)
    last_day_of_month = date(today.year, today.month + 1, 1) - timedelta(days=1)
    st.sidebar.date_input(
        "Select a date range",
        value=(first_day_of_month, last_day_of_month),
        key="date_range_filter",
        help="Select a date range to visualize",
    )
