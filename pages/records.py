import streamlit as st
import numpy as np

st.title("Wealth Tracker")

st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2")

if st.checkbox("Show dataframe"):
    dataframe = np.random.randn(10, 20)
    st.dataframe(dataframe)

x = st.slider("x")  # 👈 this is a widget
st.write(x, "squared is", x * x)

st.text_input("Your name", key="name")

# You can access the value at any point with:
st.session_state.name
