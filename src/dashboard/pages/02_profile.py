import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

st.set_page_config(page_title="Company Profile", page_icon="🏢", layout="wide")

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

df = companies.merge(
    ratios,
    on="company_id",
    how="left"
)

# ----------------------------
# Header
# ----------------------------

st.title("🏢 Company Profile")

st.caption("Search and analyze an individual company")

st.divider()

# ----------------------------
# Company Search
# ----------------------------

company = st.selectbox(
    "Select Company",
    sorted(df["company_name"].unique())
)

data = df[df["company_name"] == company].iloc[0]

# ----------------------------
# Company Information
# ----------------------------

st.subheader(data["company_name"])

c1, c2, c3 = st.columns(3)

c1.info(f"**Sector**\n\n{data['sector']}")
c2.info(f"**Industry**\n\n{data['industry']}")
c3.info(f"**Ticker**\n\n{data['ticker']}")

st.divider()

# ----------------------------
# KPI Cards
# ----------------------------

st.subheader("Key Financial Metrics")

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "ROE",
    f"{data['return_on_equity_pct']:.2f}%"
)

k2.metric(
    "ROA",
    f"{data['return_on_assets_pct']:.2f}%"
)

k3.metric(
    "Net Profit Margin",
    f"{data['net_profit_margin_pct']:.2f}%"
)

k4.metric(
    "Revenue CAGR",
    f"{data['revenue_cagr_5yr']:.2f}%"
)

st.divider()

# ----------------------------
# Financial Metrics Chart
# ----------------------------

st.subheader("Financial Snapshot")

chart = pd.DataFrame({
    "Metric": [
        "ROE",
        "ROA",
        "Profit Margin",
        "Revenue CAGR",
        "PAT CAGR",
        "EPS CAGR"
    ],
    "Value": [
        data["return_on_equity_pct"],
        data["return_on_assets_pct"],
        data["net_profit_margin_pct"],
        data["revenue_cagr_5yr"],
        data["pat_cagr_5yr"],
        data["eps_cagr_5yr"]
    ]
})

fig = px.bar(
    chart,
    x="Metric",
    y="Value",
    color="Value",
    text="Value"
)

fig.update_layout(
    coloraxis_showscale=False,
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ----------------------------
# Company Strengths
# ----------------------------

st.subheader("Quality Assessment")

left, right = st.columns(2)

with left:

    st.success(f"Quality Score : {data['quality_score']}")

    st.write("### Strengths")

    if data["return_on_equity_pct"] >= 15:
        st.success("✔ Strong Return on Equity")

    if data["net_profit_margin_pct"] >= 15:
        st.success("✔ Healthy Profit Margin")

    if data["debt_to_equity"] <= 1:
        st.success("✔ Low Debt")

with right:

    st.write("### Risk Indicators")

    if data["debt_to_equity"] > 1:
        st.error("High Debt")

    if data["interest_coverage"] < 2:
        st.error("Weak Interest Coverage")

    if data["fcf_conversion_pct"] < 50:
        st.warning("Poor Cash Flow Conversion")

st.divider()

# ----------------------------
# Complete Financial Data
# ----------------------------

with st.expander("View Complete Financial Information"):

    st.dataframe(
        data.to_frame().T,
        use_container_width=True,
        hide_index=True
    )