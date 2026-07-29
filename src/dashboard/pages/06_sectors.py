import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from io import BytesIO

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="Sector Analysis",
    page_icon="🏭",
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

# Quality_Score is stored as A/B/C in your database.
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

st.title("🏭 Sector Analysis")

st.caption(
    "Compare the financial strength of different market sectors."
)

st.divider()

# ----------------------------------------------------
# SECTOR SUMMARY
# ----------------------------------------------------

sector_df = (
    df.groupby("sector", as_index=False)
      .agg(
        Companies=("company_name", "count"),
        Market_Cap=("market_cap_cr", "sum"),
        ROE=("return_on_equity_pct", "mean"),
        ROA=("return_on_assets_pct", "mean"),
        Margin=("net_profit_margin_pct", "mean"),
        Revenue_CAGR=("revenue_cagr_5yr", "mean"),
        Quality_Score=("quality_score", "mean")
      )
)

sector_df.rename(
    columns={
        "company_name": "Companies",
        "market_cap_cr": "Market_Cap",
        "return_on_equity_pct": "ROE",
        "return_on_assets_pct": "ROA",
        "net_profit_margin_pct": "Margin",
        "revenue_cagr_5yr": "Revenue_CAGR",
        "quality_score": "Quality_Score"
    },
    inplace=True
)

# ----------------------------------------------------
# KPI CARDS
# ----------------------------------------------------

st.subheader("Sector Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Sectors",
    len(sector_df)
)

c2.metric(
    "Companies",
    len(df)
)

c3.metric(
    "Average ROE",
    f"{sector_df['ROE'].mean():.2f}%"
)

c4.metric(
    "Average Revenue_CAGR",
    f"{sector_df['Revenue_CAGR'].mean():.2f}%"
)

st.divider()

# ----------------------------------------------------
# Market_Cap
# ----------------------------------------------------

st.subheader("Sector-wise Market_Capitalization")

fig1 = px.bar(
    sector_df.sort_values(
        "Market_Cap",
        ascending=False
    ),
    x="sector",
    y="Market_Cap",
    color="sector",
    text="Market_Cap"
)

fig1.update_layout(
    height=500,
    showlegend=False,
    xaxis_title="Sector"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.divider()
# ----------------------------------------------------
# AVERAGE ROE BY SECTOR
# ----------------------------------------------------

st.subheader("Average ROE by Sector")

fig2 = px.bar(
    sector_df.sort_values(
        "ROE",
        ascending=False
    ),
    x="sector",
    y="ROE",
    color="sector",
    text="ROE"
)

fig2.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig2.update_layout(
    height=450,
    showlegend=False,
    xaxis_title="Sector",
    yaxis_title="ROE (%)"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# Revenue_CAGR BY SECTOR
# ----------------------------------------------------

st.subheader("Average Revenue_CAGR by Sector")

fig3 = px.bar(
    sector_df.sort_values(
        "Revenue_CAGR",
        ascending=False
    ),
    x="sector",
    y="Revenue_CAGR",
    color="sector",
    text="Revenue_CAGR"
)

fig3.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig3.update_layout(
    height=450,
    showlegend=False,
    xaxis_title="Sector",
    yaxis_title="Revenue_CAGR (%)"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# PROFIT MARGIN ANALYSIS
# ----------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("Average Net Profit Margin")

    fig4 = px.bar(
        sector_df.sort_values(
            "Margin",
            ascending=False
        ),
        x="sector",
        y="Margin",
        color="sector",
        text="Margin"
    )

    fig4.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig4.update_layout(
        height=420,
        showlegend=False,
        xaxis_title="Sector",
        yaxis_title="Margin (%)"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

with right:

    st.subheader("Sector Distribution")

    sector_count = (
        df.groupby("sector")
        .size()
        .reset_index(name="Companies")
    )

    fig5 = px.pie(
        sector_count,
        names="sector",
        values="Companies",
        hole=0.45
    )

    fig5.update_layout(
        height=420
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

st.divider()

# ----------------------------------------------------
# SECTOR PERFORMANCE TABLE
# ----------------------------------------------------

st.subheader("Sector Performance")

performance = sector_df.copy()

performance = performance.sort_values(
    "Quality_Score",
    ascending=False
)

st.dataframe(
    performance,
    use_container_width=True,
    hide_index=True
)

st.divider()
# ----------------------------------------------------
# SECTOR RANKING
# ----------------------------------------------------

st.subheader("🏆 Sector Ranking")

ranking_df = sector_df.copy()
ranking_df = ranking_df.fillna(0)

ranking_df["Sector Score"] = (
    ranking_df["ROE"] * 0.30 +
    ranking_df["ROA"] * 0.15 +
    ranking_df["Margin"] * 0.20 +
    ranking_df["Revenue_CAGR"] * 0.20 +
    ranking_df["Quality_Score"] * 3 +
    (ranking_df["Market_Cap"] / 100000)
)

ranking_df = ranking_df.sort_values(
    "Sector Score",
    ascending=False
).reset_index(drop=True)

ranking_df["Rank"] = ranking_df.index + 1

ranking = ranking_df[
    [
        "Rank",
        "sector",
        "Companies",
        "Market_Cap",
        "ROE",
        "ROA",
        "Margin",
        "Revenue_CAGR",
        "Quality_Score",
        "Sector Score"
    ]
].copy()

ranking.columns = [
    "Rank",
    "Sector",
    "Companies",
    "Market_Cap (Cr)",
    "Average ROE (%)",
    "Average ROA (%)",
    "Average Margin (%)",
    "Revenue_CAGR (%)",
    "Quality_Score",
    "Sector Score"
]

st.dataframe(
    ranking,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ----------------------------------------------------
# BEST SECTOR
# ----------------------------------------------------

winner = ranking_df.iloc[0]

st.success(
    f"""
🏆 Best Performing Sector

**{winner['sector']}**

Sector Score : **{winner['Sector Score']:.2f}**

Average ROE : **{winner['ROE']:.2f}%**

Revenue_CAGR : **{winner['Revenue_CAGR']:.2f}%**

Quality_Score : **{winner['Quality_Score']:.2f}**
"""
)

st.divider()

# ----------------------------------------------------
# DOWNLOADS
# ----------------------------------------------------

st.subheader("Download Sector Report")

csv = ranking.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📄 Download CSV",
    data=csv,
    file_name="sector_analysis.csv",
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
        sheet_name="Sector Analysis"
    )

st.download_button(
    label="📊 Download Excel",
    data=excel_buffer.getvalue(),
    file_name="sector_analysis.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.divider()

# ----------------------------------------------------
# SECTOR INSIGHTS
# ----------------------------------------------------

st.subheader("Sector Insights")

best_roe = sector_df.loc[
    sector_df["ROE"].idxmax(),
    "sector"
]

best_margin = sector_df.loc[
    sector_df["Margin"].idxmax(),
    "sector"
]

best_growth = sector_df.loc[
    sector_df["Revenue_CAGR"].idxmax(),
    "sector"
]

largest_sector = sector_df.loc[
    sector_df["Market_Cap"].idxmax(),
    "sector"
]

st.info(
    f"""
🏆 Highest Average ROE : **{best_roe}**

💰 Highest Profit Margin : **{best_margin}**

📈 Highest Revenue_CAGR : **{best_growth}**

🏢 Largest Market_Capitalization : **{largest_sector}**
"""
)

st.divider()

# ----------------------------------------------------
# SUMMARY
# ----------------------------------------------------

st.subheader("Summary")

st.write(
    """
The Sector Analysis dashboard compares all market sectors using
key financial indicators such as ROE, ROA, Profit Margin,
Revenue_CAGR, Market_Capitalization, and Quality_Score.
This helps identify sectors that demonstrate stronger profitability,
growth potential, and financial stability.
"""
)

st.divider()

# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------

st.caption(
    "Financial Intelligence Platform • Sector Analysis Dashboard"
)