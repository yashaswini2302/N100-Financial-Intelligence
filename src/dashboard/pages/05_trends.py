import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="Trend Analysis",
    page_icon="📈",
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
# -------------------------------
# Convert numeric columns
# -------------------------------

numeric_columns = [
    "market_cap_cr",
    "return_on_equity_pct",
    "return_on_assets_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "interest_coverage",
    "asset_turnover",
    "free_cash_flow_cr",
    "fcf_conversion_pct",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "eps_cagr_5yr"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Quality score is stored as A/B/C in your database.
quality_map = {
    "A+": 10,
    "A": 9,
    "B+": 8,
    "B": 7,
    "C+": 6,
    "C": 5,
    "D": 4
}

if "quality_score" in df.columns:
    if df["quality_score"].dtype == object:
        df["quality_score"] = (
            df["quality_score"]
            .astype(str)
            .str.strip()
            .map(quality_map)
        )

    df["quality_score"] = pd.to_numeric(
        df["quality_score"],
        errors="coerce"
    ).fillna(0)
# ----------------------------------------------------
# TITLE
# ----------------------------------------------------

st.title("📈 Trend Analysis")

st.caption(
    "Analyze financial growth and profitability trends across companies."
)

st.divider()

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

st.sidebar.header("Trend Filters")

sector = st.sidebar.selectbox(
    "Sector",
    ["All"] + sorted(df["sector"].unique())
)

if sector == "All":
    filtered = df.copy()
else:
    filtered = df[df["sector"] == sector]

selected = st.sidebar.multiselect(
    "Select Companies",
    filtered["company_name"],
    default=filtered["company_name"].head(5).tolist()
)

trend_df = filtered[
    filtered["company_name"].isin(selected)
].copy()

if len(trend_df) == 0:
    st.warning("Please select at least one company.")
    st.stop()

# ----------------------------------------------------
# KPI CARDS
# ----------------------------------------------------

st.subheader("Growth Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Companies",
    len(trend_df)
)

c2.metric(
    "Average Revenue CAGR",
    f"{trend_df['revenue_cagr_5yr'].mean():.2f}%"
)

c3.metric(
    "Average PAT CAGR",
    f"{trend_df['pat_cagr_5yr'].mean():.2f}%"
)

c4.metric(
    "Average ROE",
    f"{trend_df['return_on_equity_pct'].mean():.2f}%"
)

st.divider()

# ----------------------------------------------------
# REVENUE CAGR CHART
# ----------------------------------------------------

st.subheader("Revenue CAGR Comparison")

fig1 = px.bar(
    trend_df.sort_values(
        "revenue_cagr_5yr",
        ascending=False
    ),
    x="company_name",
    y="revenue_cagr_5yr",
    color="sector",
    text="revenue_cagr_5yr"
)

fig1.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig1.update_layout(
    height=500,
    xaxis_title="",
    yaxis_title="Revenue CAGR (%)"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.divider()
# ----------------------------------------------------
# PAT CAGR COMPARISON
# ----------------------------------------------------

st.subheader("PAT CAGR Comparison")

fig2 = px.bar(
    trend_df.sort_values(
        "pat_cagr_5yr",
        ascending=False
    ),
    x="company_name",
    y="pat_cagr_5yr",
    color="sector",
    text="pat_cagr_5yr"
)

fig2.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig2.update_layout(
    height=500,
    xaxis_title="",
    yaxis_title="PAT CAGR (%)"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# ROE VS ROA
# ----------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("Return on Equity")

    fig3 = px.bar(
        trend_df.sort_values(
            "return_on_equity_pct",
            ascending=False
        ),
        x="company_name",
        y="return_on_equity_pct",
        color="company_name",
        text="return_on_equity_pct"
    )

    fig3.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig3.update_layout(
        height=420,
        showlegend=False,
        xaxis_title="",
        yaxis_title="ROE (%)"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with right:

    st.subheader("Return on Assets")

    fig4 = px.bar(
        trend_df.sort_values(
            "return_on_assets_pct",
            ascending=False
        ),
        x="company_name",
        y="return_on_assets_pct",
        color="company_name",
        text="return_on_assets_pct"
    )

    fig4.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig4.update_layout(
        height=420,
        showlegend=False,
        xaxis_title="",
        yaxis_title="ROA (%)"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

st.divider()

# ----------------------------------------------------
# PROFITABILITY ANALYSIS
# ----------------------------------------------------

st.subheader("Profitability Analysis")

fig5 = px.scatter(
    trend_df,
    x="return_on_equity_pct",
    y="net_profit_margin_pct",
    size="market_cap_cr",
    color="sector",
    hover_name="company_name",
    text="company_name"
)

fig5.update_traces(
    textposition="top center"
)

fig5.update_layout(
    height=600,
    xaxis_title="ROE (%)",
    yaxis_title="Net Profit Margin (%)"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# PERFORMANCE TABLE
# ----------------------------------------------------

st.subheader("Growth Performance")

performance = trend_df[
    [
        "company_name",
        "sector",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "return_on_equity_pct",
        "return_on_assets_pct",
        "net_profit_margin_pct",
        "quality_score"
    ]
].copy()

performance.columns = [
    "Company",
    "Sector",
    "Revenue CAGR (%)",
    "PAT CAGR (%)",
    "ROE (%)",
    "ROA (%)",
    "Net Profit Margin (%)",
    "Quality Score"
]

performance = performance.sort_values(
    "Revenue CAGR (%)",
    ascending=False
)

st.dataframe(
    performance,
    use_container_width=True,
    hide_index=True
)

st.divider()
# ----------------------------------------------------
# GROWTH SCORE
# ----------------------------------------------------

st.subheader("🏆 Overall Growth Ranking")

ranking_df = trend_df.copy()
ranking_df = ranking_df.fillna(0)

ranking_df["Growth Score"] = (
    ranking_df["revenue_cagr_5yr"] * 0.35 +
    ranking_df["pat_cagr_5yr"] * 0.30 +
    ranking_df["return_on_equity_pct"] * 0.20 +
    ranking_df["return_on_assets_pct"] * 0.10 +
    ranking_df["quality_score"] * 1.50 +
    ranking_df["net_profit_margin_pct"] * 0.05
)

ranking_df = ranking_df.sort_values(
    "Growth Score",
    ascending=False
).reset_index(drop=True)

ranking_df["Rank"] = ranking_df.index + 1

ranking = ranking_df[
    [
        "Rank",
        "company_name",
        "Growth Score",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "return_on_equity_pct",
        "quality_score"
    ]
].copy()

ranking.columns = [
    "Rank",
    "Company",
    "Growth Score",
    "Revenue CAGR (%)",
    "PAT CAGR (%)",
    "ROE (%)",
    "Quality Score"
]

st.dataframe(
    ranking,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ----------------------------------------------------
# BEST PERFORMER
# ----------------------------------------------------

winner = ranking_df.iloc[0]

st.success(
    f"""
🏆 Best Growth Company

**{winner['company_name']}**

Growth Score : **{winner['Growth Score']:.2f}**

Revenue CAGR : **{winner['revenue_cagr_5yr']:.2f}%**

PAT CAGR : **{winner['pat_cagr_5yr']:.2f}%**

ROE : **{winner['return_on_equity_pct']:.2f}%**

Quality Score : **{winner['quality_score']}**
"""
)

st.divider()

# ----------------------------------------------------
# DOWNLOADS
# ----------------------------------------------------

st.subheader("Download Report")

csv = ranking.to_csv(index=False).encode("utf-8")

st.download_button(
    "📄 Download CSV",
    csv,
    "trend_analysis.csv",
    "text/csv"
)

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    ranking.to_excel(
        writer,
        index=False,
        sheet_name="Trend Analysis"
    )

st.download_button(
    "📊 Download Excel",
    excel_buffer.getvalue(),
    "trend_analysis.xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.divider()

# ----------------------------------------------------
# TREND INSIGHTS
# ----------------------------------------------------

st.subheader("Trend Insights")

highest_revenue = trend_df.loc[
    trend_df["revenue_cagr_5yr"].idxmax(),
    "company_name"
]

highest_pat = trend_df.loc[
    trend_df["pat_cagr_5yr"].idxmax(),
    "company_name"
]

highest_roe = trend_df.loc[
    trend_df["return_on_equity_pct"].idxmax(),
    "company_name"
]

highest_margin = trend_df.loc[
    trend_df["net_profit_margin_pct"].idxmax(),
    "company_name"
]

st.info(
    f"""
📈 Highest Revenue CAGR : **{highest_revenue}**

💹 Highest PAT CAGR : **{highest_pat}**

🏆 Highest ROE : **{highest_roe}**

💰 Highest Net Profit Margin : **{highest_margin}**
"""
)

st.divider()

# ----------------------------------------------------
# SUMMARY
# ----------------------------------------------------

st.subheader("Summary")

st.write(
    """
This dashboard helps identify companies with consistent financial growth by
comparing Revenue CAGR, PAT CAGR, ROE, ROA, Profit Margin, and Quality Score.
Higher ranked companies generally demonstrate stronger long-term financial
performance and operational efficiency.
    """
)

st.divider()

st.caption(
    "Financial Intelligence Platform • Trend Analysis Dashboard"
)
