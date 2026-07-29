import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

# ----------------------------
# Database
# ----------------------------

conn = sqlite3.connect("data/db/nifty100.db")

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

# ----------------------------
# Merge Data
# ----------------------------

df = ratios.merge(
    companies,
    on="company_id",
    how="left"
)

# ----------------------------
# Header
# ----------------------------

st.title("📊 N100 Financial Intelligence Dashboard")
st.caption("Real-time overview of company financial performance")

st.divider()

# ----------------------------
# KPI Cards
# ----------------------------

st.subheader("Market Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Companies",
    df["company_id"].nunique()
)

c2.metric(
    "Average ROE",
    f"{df['return_on_equity_pct'].mean():.2f}%"
)

c3.metric(
    "Average Net Profit Margin",
    f"{df['net_profit_margin_pct'].mean():.2f}%"
)

c4.metric(
    "Average Revenue CAGR",
    f"{df['revenue_cagr_5yr'].mean():.2f}%"
)

st.divider()

# ----------------------------
# Charts
# ----------------------------

left, right = st.columns(2)

with left:

    st.subheader("Sector Distribution")

    sector = (
        df.groupby("sector")
        .size()
        .reset_index(name="Companies")
    )

    fig = px.pie(
        sector,
        names="sector",
        values="Companies",
        hole=0.55
    )

    fig.update_layout(
        height=450,
        showlegend=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("Top 10 Companies by ROE")

    top = (
        df.sort_values(
            "return_on_equity_pct",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        top,
        x="company_name",
        y="return_on_equity_pct",
        color="return_on_equity_pct",
        text="return_on_equity_pct"
    )

    fig.update_layout(
        xaxis_title="Company",
        yaxis_title="ROE (%)",
        coloraxis_showscale=False,
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ----------------------------
# Best Companies
# ----------------------------

st.subheader("🏆 Top Quality Companies")

best = df.sort_values(
    "return_on_equity_pct",
    ascending=False
)[[
    "company_name",
    "sector",
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "revenue_cagr_5yr"
]].head(10)

st.dataframe(
    best,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ----------------------------
# Full Dataset
# ----------------------------

with st.expander("View Financial Ratios Dataset"):

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )