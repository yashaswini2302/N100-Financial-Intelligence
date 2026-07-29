import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from io import BytesIO

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="Executive Reports",
    page_icon="📄",
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

st.title("📄 Executive Reports")

st.caption(
    "Comprehensive financial intelligence summary for all companies."
)

st.divider()

# ----------------------------------------------------
# KPI CARDS
# ----------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Companies",
    len(df)
)

c2.metric(
    "Sectors",
    df["sector"].nunique()
)

c3.metric(
    "Average ROE",
    f"{df['return_on_equity_pct'].mean():.2f}%"
)

c4.metric(
    "Average Quality",
    f"{df['quality_score'].mean():.2f}"
)

st.divider()

# ----------------------------------------------------
# EXECUTIVE SCORE
# ----------------------------------------------------

report_df = df.copy()
report_df = report_df.fillna(0)

report_df["Executive Score"] = (
    report_df["return_on_equity_pct"] * 0.25 +
    report_df["return_on_assets_pct"] * 0.15 +
    report_df["net_profit_margin_pct"] * 0.15 +
    report_df["revenue_cagr_5yr"] * 0.15 +
    report_df["pat_cagr_5yr"] * 0.10 +
    report_df["quality_score"] * 3 -
    report_df["debt_to_equity"] * 10
)

report_df = report_df.sort_values(
    "Executive Score",
    ascending=False
)

# ----------------------------------------------------
# TOP 10 COMPANIES
# ----------------------------------------------------

st.subheader("Top 10 Companies")

top10 = report_df.head(10)

fig = px.bar(
    top10,
    x="company_name",
    y="Executive Score",
    color="sector",
    text="Executive Score"
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig.update_layout(
    height=500,
    xaxis_title="Company"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()
# ----------------------------------------------------
# SECTOR PERFORMANCE
# ----------------------------------------------------

st.subheader("Sector Performance")

sector_summary = (
    report_df.groupby("sector")
    .agg(
        Companies=("company_name", "count"),
        Avg_ROE=("return_on_equity_pct", "mean"),
        Avg_ROA=("return_on_assets_pct", "mean"),
        Avg_Margin=("net_profit_margin_pct", "mean"),
        Avg_Growth=("revenue_cagr_5yr", "mean"),
        Avg_Quality=("quality_score", "mean")
    )
    .reset_index()
)

fig2 = px.bar(
    sector_summary.sort_values(
        "Avg_ROE",
        ascending=False
    ),
    x="sector",
    y="Avg_ROE",
    color="sector",
    text="Avg_ROE"
)

fig2.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig2.update_layout(
    height=450,
    showlegend=False,
    xaxis_title="Sector",
    yaxis_title="Average ROE (%)"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# TOP PERFORMERS
# ----------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("Top ROE Companies")

    top_roe = report_df.nlargest(
        10,
        "return_on_equity_pct"
    )

    fig3 = px.bar(
        top_roe,
        x="company_name",
        y="return_on_equity_pct",
        color="sector",
        text="return_on_equity_pct"
    )

    fig3.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig3.update_layout(
        height=450,
        xaxis_title="Company",
        yaxis_title="ROE (%)"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with right:

    st.subheader("Highest Profit Margin")

    top_margin = report_df.nlargest(
        10,
        "net_profit_margin_pct"
    )

    fig4 = px.bar(
        top_margin,
        x="company_name",
        y="net_profit_margin_pct",
        color="sector",
        text="net_profit_margin_pct"
    )

    fig4.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig4.update_layout(
        height=450,
        xaxis_title="Company",
        yaxis_title="Net Profit Margin (%)"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

st.divider()

# ----------------------------------------------------
# EXECUTIVE REPORT TABLE
# ----------------------------------------------------

st.subheader("Executive Ranking")

ranking = report_df[
    [
        "company_name",
        "sector",
        "Executive Score",
        "return_on_equity_pct",
        "return_on_assets_pct",
        "net_profit_margin_pct",
        "revenue_cagr_5yr",
        "quality_score"
    ]
].copy()

ranking.columns = [
    "Company",
    "Sector",
    "Executive Score",
    "ROE (%)",
    "ROA (%)",
    "Net Profit Margin (%)",
    "Revenue CAGR (%)",
    "Quality Score"
]

ranking = ranking.sort_values(
    "Executive Score",
    ascending=False
)

st.dataframe(
    ranking,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ----------------------------------------------------
# EXECUTIVE SCORE DISTRIBUTION
# ----------------------------------------------------

st.subheader("Executive Score Distribution")

fig5 = px.histogram(
    report_df,
    x="Executive Score",
    nbins=10,
    color="sector"
)

fig5.update_layout(
    height=450
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.divider()
# ----------------------------------------------------
# BEST COMPANY
# ----------------------------------------------------

st.subheader("🏆 Executive Summary")

best = report_df.iloc[0]

st.success(
    f"""
🏆 Best Overall Company

**{best['company_name']}**

Executive Score : **{best['Executive Score']:.2f}**

Sector : **{best['sector']}**

ROE : **{best['return_on_equity_pct']:.2f}%**

ROA : **{best['return_on_assets_pct']:.2f}%**

Net Profit Margin : **{best['net_profit_margin_pct']:.2f}%**

Revenue CAGR : **{best['revenue_cagr_5yr']:.2f}%**

Quality Score : **{best['quality_score']}**
"""
)

st.divider()

# ----------------------------------------------------
# DOWNLOAD REPORT
# ----------------------------------------------------

st.subheader("Download Executive Report")

csv = ranking.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📄 Download CSV",
    data=csv,
    file_name="executive_report.csv",
    mime="text/csv"
)

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:

    ranking.to_excel(
        writer,
        index=False,
        sheet_name="Executive Report"
    )

st.download_button(
    label="📊 Download Excel",
    data=excel_buffer.getvalue(),
    file_name="executive_report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.divider()

# ----------------------------------------------------
# KEY INSIGHTS
# ----------------------------------------------------

st.subheader("Executive Insights")

highest_roe = report_df.loc[
    report_df["return_on_equity_pct"].idxmax(),
    "company_name"
]

highest_margin = report_df.loc[
    report_df["net_profit_margin_pct"].idxmax(),
    "company_name"
]

highest_growth = report_df.loc[
    report_df["revenue_cagr_5yr"].idxmax(),
    "company_name"
]

lowest_debt = report_df.loc[
    report_df["debt_to_equity"].idxmin(),
    "company_name"
]

highest_quality = report_df.loc[
    report_df["quality_score"].idxmax(),
    "company_name"
]

largest_company = report_df.loc[
    report_df["market_cap_cr"].idxmax(),
    "company_name"
]

st.info(
    f"""
🏆 Highest ROE : **{highest_roe}**

💰 Highest Net Profit Margin : **{highest_margin}**

📈 Highest Revenue CAGR : **{highest_growth}**

🛡 Lowest Debt / Equity : **{lowest_debt}**

⭐ Highest Quality Score : **{highest_quality}**

🏢 Largest Market Capitalization : **{largest_company}**
"""
)

st.divider()

# ----------------------------------------------------
# OVERALL STATISTICS
# ----------------------------------------------------

st.subheader("Overall Statistics")

stats = pd.DataFrame({
    "Metric": [
        "Average ROE",
        "Average ROA",
        "Average Net Profit Margin",
        "Average Revenue CAGR",
        "Average PAT CAGR",
        "Average Debt / Equity",
        "Average Asset Turnover",
        "Average Interest Coverage",
        "Average Quality Score"
    ],
    "Value": [
        round(report_df["return_on_equity_pct"].mean(), 2),
        round(report_df["return_on_assets_pct"].mean(), 2),
        round(report_df["net_profit_margin_pct"].mean(), 2),
        round(report_df["revenue_cagr_5yr"].mean(), 2),
        round(report_df["pat_cagr_5yr"].mean(), 2),
        round(report_df["debt_to_equity"].mean(), 2),
        round(report_df["asset_turnover"].mean(), 2),
        round(report_df["interest_coverage"].mean(), 2),
        round(report_df["quality_score"].mean(), 2)
    ]
})

st.dataframe(
    stats,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ----------------------------------------------------
# CONCLUSION
# ----------------------------------------------------

st.subheader("Conclusion")

st.write(
    """
The Executive Report consolidates the financial performance of all companies
into a single dashboard. It combines profitability, growth, capital
efficiency, and quality metrics to provide an overall view of business
performance.

Use this report to:
- Identify the strongest companies.
- Compare sectors.
- Evaluate financial health.
- Analyze long-term growth potential.
- Support investment research and decision-making.
"""
)

st.divider()

# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------

st.caption(
    "Financial Intelligence Platform • Executive Reports Dashboard • Sprint 4"
)