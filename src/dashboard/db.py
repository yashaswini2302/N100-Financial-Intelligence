import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "data/db/nifty100.db"


@st.cache_data(ttl=600)
def load_table(table_name):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_financial_ratios():
    return load_table("financial_ratios")


@st.cache_data(ttl=600)
def get_companies():
    return load_table("companies")


@st.cache_data(ttl=600)
def get_peer_groups():
    return load_table("peer_groups")


@st.cache_data(ttl=600)
def get_peer_percentiles():
    return load_table("peer_percentiles")