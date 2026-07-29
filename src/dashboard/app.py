import streamlit as st

st.set_page_config(
    page_title="N100 Financial Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 N100 Financial Intelligence Platform")

st.write("""
Welcome to the N100 Financial Intelligence Dashboard.

Use the sidebar to navigate through the available pages.
""")

st.success("Dashboard loaded successfully.")