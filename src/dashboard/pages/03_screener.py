import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from io import BytesIO

st.set_page_config(
    page_title="Smart Screener",
    page_icon="🔍",
    layout="wide"
)

# ----------------------------------------------------
# DATABASE
# ----------------------------------------------------

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

# ----------------------------------------------------
# TITLE
# ----------------------------------------------------

st.title("🔍 Smart Stock Screener")

st.caption(
    "Filter companies using financial metrics and quality parameters."
)

st.divider()

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

st.sidebar.header("Filters")

sector = st.sidebar.multiselect(
    "Sector",
    sorted(df["sector"].unique()),
    default=sorted(df["sector"].unique())
)

quality = st.sidebar.multiselect(
    "Quality Score",
    sorted(df["quality_score"].unique()),
    default=sorted(df["quality_score"].unique())
)

min_roe = st.sidebar.slider(
    "Minimum ROE (%)",
    0.0,
    float(df["return_on_equity_pct"].max()),
    10.0
)

min_roa = st.sidebar.slider(
    "Minimum ROA (%)",
    0.0,
    float(df["return_on_assets_pct"].max()),
    2.0
)

min_margin = st.sidebar.slider(
    "Minimum Net Profit Margin (%)",
    0.0,
    float(df["net_profit_margin_pct"].max()),
    5.0
)

max_debt = st.sidebar.slider(
    "Maximum Debt / Equity",
    0.0,
    float(df["debt_to_equity"].max()),
    float(df["debt_to_equity"].max())
)

min_growth = st.sidebar.slider(
    "Minimum Revenue CAGR (%)",
    0.0,
    float(df["revenue_cagr_5yr"].max()),
    5.0
)

# ----------------------------------------------------
# FILTER DATA
# ----------------------------------------------------

filtered = df[
    (df["sector"].isin(sector)) &
    (df["quality_score"].isin(quality)) &
    (df["return_on_equity_pct"] >= min_roe) &
    (df["return_on_assets_pct"] >= min_roa) &
    (df["net_profit_margin_pct"] >= min_margin) &
    (df["debt_to_equity"] <= max_debt) &
    (df["revenue_cagr_5yr"] >= min_growth)
]

# ----------------------------------------------------
# KPI CARDS
# ----------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Companies Found",
    len(filtered)
)

c2.metric(
    "Average ROE",
    f"{filtered['return_on_equity_pct'].mean():.2f}%"
    if len(filtered) else "0%"
)

c3.metric(
    "Average Margin",
    f"{filtered['net_profit_margin_pct'].mean():.2f}%"
    if len(filtered) else "0%"
)

c4.metric(
    "Average Debt/Equity",
    f"{filtered['debt_to_equity'].mean():.2f}"
    if len(filtered) else "0"
)

st.divider()

# ----------------------------------------------------
# QUICK FILTERS
# ----------------------------------------------------

st.subheader("⭐ Quick Screeners")

q1, q2, q3, q4 = st.columns(4)

if q1.button("Quality Compounders"):
    filtered = df[
        (df["return_on_equity_pct"] > 20) &
        (df["debt_to_equity"] < 0.5)
    ]

if q2.button("Growth Stocks"):
    filtered = df[
        df["revenue_cagr_5yr"] > 15
    ]

if q3.button("Low Debt"):
    filtered = df[
        df["debt_to_equity"] < 0.30
    ]

if q4.button("High Margin"):
    filtered = df[
        df["net_profit_margin_pct"] > 20
    ]

st.divider()

# ----------------------------------------------------
# CHARTS
# ----------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("ROE Distribution")

    fig = px.histogram(
        filtered,
        x="return_on_equity_pct",
        nbins=10,
        color="quality_score"
    )

    fig.update_layout(height=420)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("Sector Distribution")

    sector_chart = (
        filtered
        .groupby("sector")
        .size()
        .reset_index(name="Companies")
    )

    fig2 = px.pie(
        sector_chart,
        names="sector",
        values="Companies"
    )

    fig2.update_layout(height=420)

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()
# ----------------------------------------------------
# QUALITY SCORE CHART
# ----------------------------------------------------

st.subheader("Quality Score Distribution")

quality_chart = (
    filtered
    .groupby("quality_score")
    .size()
    .reset_index(name="Companies")
)

fig3 = px.bar(
    quality_chart,
    x="quality_score",
    y="Companies",
    color="quality_score",
    text="Companies"
)

fig3.update_layout(
    height=420,
    coloraxis_showscale=False
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# SORT OPTIONS
# ----------------------------------------------------

st.subheader("Screening Results")

sort_col1, sort_col2 = st.columns([2, 1])

sort_column = sort_col1.selectbox(
    "Sort By",
    [
        "return_on_equity_pct",
        "return_on_assets_pct",
        "net_profit_margin_pct",
        "revenue_cagr_5yr",
        "debt_to_equity",
    ],
)

ascending = sort_col2.selectbox(
    "Order",
    ["Descending", "Ascending"]
)

filtered = filtered.sort_values(
    by=sort_column,
    ascending=(ascending == "Ascending")
)

# ----------------------------------------------------
# DISPLAY TABLE
# ----------------------------------------------------

display = filtered[
    [
        "company_name",
        "sector",
        "return_on_equity_pct",
        "return_on_assets_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "quality_score",
    ]
].copy()

display.columns = [
    "Company",
    "Sector",
    "ROE (%)",
    "ROA (%)",
    "Net Profit Margin (%)",
    "Debt / Equity",
    "Revenue CAGR (%)",
    "Quality",
]

st.dataframe(
    display,
    use_container_width=True,
    hide_index=True
)

# ----------------------------------------------------
# DOWNLOADS
# ----------------------------------------------------

st.divider()

st.subheader("Download Results")

csv = display.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📄 Download CSV",
    data=csv,
    file_name="screening_results.csv",
    mime="text/csv",
)

excel_buffer = BytesIO()

with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
    display.to_excel(writer, index=False, sheet_name="Screening Results")

st.download_button(
    label="📊 Download Excel",
    data=excel_buffer.getvalue(),
    file_name="screening_results.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)

# ----------------------------------------------------
# SUMMARY
# ----------------------------------------------------

st.divider()

st.subheader("Summary")

if len(display) == 0:
    st.warning("No companies match the selected filters.")
else:
    st.success(
        f"{len(display)} companies matched your screening criteria."
    )

    best = display.iloc[0]

    st.info(
        f"Top ranked company: **{best['Company']}** "
        f"(ROE: {best['ROE (%)']:.2f}%)"
    )

st.caption("Financial Intelligence Platform • Smart Screener")