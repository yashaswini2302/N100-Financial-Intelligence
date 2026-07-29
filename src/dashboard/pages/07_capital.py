import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from io import BytesIO

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="Capital Allocation",
    page_icon="💰",
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

st.title("💰 Capital Allocation Dashboard")

st.caption(
    "Analyze how efficiently companies allocate capital using debt, cash flow and asset utilization metrics."
)

st.divider()

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

st.sidebar.header("Filters")

sector = st.sidebar.selectbox(
    "Sector",
    ["All"] + sorted(df["sector"].unique())
)

if sector == "All":
    filtered = df.copy()
else:
    filtered = df[df["sector"] == sector]

selected = st.sidebar.multiselect(
    "Companies",
    filtered["company_name"],
    default=filtered["company_name"].head(5).tolist()
)

capital_df = filtered[
    filtered["company_name"].isin(selected)
].copy()

if len(capital_df) == 0:
    st.warning("Please select at least one company.")
    st.stop()

# ----------------------------------------------------
# KPI CARDS
# ----------------------------------------------------

st.subheader("Capital Efficiency Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Companies",
    len(capital_df)
)

c2.metric(
    "Average Asset Turnover",
    f"{capital_df['asset_turnover'].mean():.2f}"
)

c3.metric(
    "Average Debt / Equity",
    f"{capital_df['debt_to_equity'].mean():.2f}"
)

c4.metric(
    "Average Interest Coverage",
    f"{capital_df['interest_coverage'].mean():.2f}"
)

st.divider()

# ----------------------------------------------------
# FREE CASH FLOW
# ----------------------------------------------------

st.subheader("Free Cash Flow")

fig1 = px.bar(
    capital_df.sort_values(
        "free_cash_flow_cr",
        ascending=False
    ),
    x="company_name",
    y="free_cash_flow_cr",
    color="sector",
    text="free_cash_flow_cr"
)

fig1.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig1.update_layout(
    height=500,
    xaxis_title="",
    yaxis_title="Free Cash Flow (Cr)"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.divider()
# ----------------------------------------------------
# ASSET TURNOVER & DEBT ANALYSIS
# ----------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("Asset Turnover")

    fig2 = px.bar(
        capital_df.sort_values(
            "asset_turnover",
            ascending=False
        ),
        x="company_name",
        y="asset_turnover",
        color="company_name",
        text="asset_turnover"
    )

    fig2.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig2.update_layout(
        height=450,
        showlegend=False,
        xaxis_title="",
        yaxis_title="Asset Turnover"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

with right:

    st.subheader("Debt to Equity")

    fig3 = px.bar(
        capital_df.sort_values(
            "debt_to_equity"
        ),
        x="company_name",
        y="debt_to_equity",
        color="company_name",
        text="debt_to_equity"
    )

    fig3.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig3.update_layout(
        height=450,
        showlegend=False,
        xaxis_title="",
        yaxis_title="Debt / Equity"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

st.divider()

# ----------------------------------------------------
# INTEREST COVERAGE & FCF CONVERSION
# ----------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("Interest Coverage")

    fig4 = px.bar(
        capital_df.sort_values(
            "interest_coverage",
            ascending=False
        ),
        x="company_name",
        y="interest_coverage",
        color="company_name",
        text="interest_coverage"
    )

    fig4.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig4.update_layout(
        height=450,
        showlegend=False,
        xaxis_title="",
        yaxis_title="Interest Coverage"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

with right:

    st.subheader("FCF Conversion")

    fig5 = px.bar(
        capital_df.sort_values(
            "fcf_conversion_pct",
            ascending=False
        ),
        x="company_name",
        y="fcf_conversion_pct",
        color="company_name",
        text="fcf_conversion_pct"
    )

    fig5.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig5.update_layout(
        height=450,
        showlegend=False,
        xaxis_title="",
        yaxis_title="FCF Conversion (%)"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

st.divider()

# ----------------------------------------------------
# CAPITAL EFFICIENCY TABLE
# ----------------------------------------------------

st.subheader("Capital Efficiency")

performance = capital_df[
    [
        "company_name",
        "sector",
        "asset_turnover",
        "debt_to_equity",
        "interest_coverage",
        "free_cash_flow_cr",
        "fcf_conversion_pct",
        "quality_score"
    ]
].copy()

performance.columns = [
    "Company",
    "Sector",
    "Asset Turnover",
    "Debt / Equity",
    "Interest Coverage",
    "Free Cash Flow (Cr)",
    "FCF Conversion (%)",
    "Quality Score"
]

performance = performance.sort_values(
    "Asset Turnover",
    ascending=False
)

st.dataframe(
    performance,
    use_container_width=True,
    hide_index=True
)

st.divider()
# ----------------------------------------------------
# CAPITAL EFFICIENCY RANKING
# ----------------------------------------------------

st.subheader("🏆 Capital Efficiency Ranking")

ranking_df = capital_df.copy()
ranking_df = ranking_df.fillna(0)

ranking_df["Capital Score"] = (
    ranking_df["asset_turnover"] * 25 +
    ranking_df["interest_coverage"] * 4 +
    ranking_df["fcf_conversion_pct"] * 0.25 +
    ranking_df["free_cash_flow_cr"] * 0.02 +
    ranking_df["quality_score"] * 3 -
    ranking_df["debt_to_equity"] * 20
)

ranking_df = ranking_df.sort_values(
    "Capital Score",
    ascending=False
).reset_index(drop=True)

ranking_df["Rank"] = ranking_df.index + 1

ranking = ranking_df[
    [
        "Rank",
        "company_name",
        "Capital Score",
        "asset_turnover",
        "interest_coverage",
        "debt_to_equity",
        "free_cash_flow_cr",
        "fcf_conversion_pct",
        "quality_score"
    ]
].copy()

ranking.columns = [
    "Rank",
    "Company",
    "Capital Score",
    "Asset Turnover",
    "Interest Coverage",
    "Debt / Equity",
    "Free Cash Flow (Cr)",
    "FCF Conversion (%)",
    "Quality Score"
]

st.dataframe(
    ranking,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ----------------------------------------------------
# BEST COMPANY
# ----------------------------------------------------

winner = ranking_df.iloc[0]

st.success(
    f"""
🏆 Best Capital Allocator

**{winner['company_name']}**

Capital Score : **{winner['Capital Score']:.2f}**

Asset Turnover : **{winner['asset_turnover']:.2f}**

Interest Coverage : **{winner['interest_coverage']:.2f}**

Debt / Equity : **{winner['debt_to_equity']:.2f}**

FCF Conversion : **{winner['fcf_conversion_pct']:.2f}%**
"""
)

st.divider()

# ----------------------------------------------------
# DOWNLOAD REPORTS
# ----------------------------------------------------

st.subheader("Download Report")

csv = ranking.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📄 Download CSV",
    data=csv,
    file_name="capital_allocation.csv",
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
        sheet_name="Capital Allocation"
    )

st.download_button(
    label="📊 Download Excel",
    data=excel_buffer.getvalue(),
    file_name="capital_allocation.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.divider()

# ----------------------------------------------------
# CAPITAL INSIGHTS
# ----------------------------------------------------

st.subheader("Capital Insights")

highest_asset = capital_df.loc[
    capital_df["asset_turnover"].idxmax(),
    "company_name"
]

lowest_debt = capital_df.loc[
    capital_df["debt_to_equity"].idxmin(),
    "company_name"
]

highest_interest = capital_df.loc[
    capital_df["interest_coverage"].idxmax(),
    "company_name"
]

highest_fcf = capital_df.loc[
    capital_df["free_cash_flow_cr"].idxmax(),
    "company_name"
]

highest_conversion = capital_df.loc[
    capital_df["fcf_conversion_pct"].idxmax(),
    "company_name"
]

st.info(
    f"""
🏭 Highest Asset Turnover : **{highest_asset}**

🛡 Lowest Debt / Equity : **{lowest_debt}**

💹 Highest Interest Coverage : **{highest_interest}**

💰 Highest Free Cash Flow : **{highest_fcf}**

📈 Highest FCF Conversion : **{highest_conversion}**
"""
)

st.divider()

# ----------------------------------------------------
# SUMMARY
# ----------------------------------------------------

st.subheader("Summary")

st.write(
    """
The Capital Allocation dashboard evaluates how efficiently companies
utilize their assets, manage debt, generate free cash flow, and convert
earnings into cash. The Capital Score provides an overall measure of
capital efficiency, helping identify financially disciplined companies.
"""
)

st.divider()

# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------

st.caption(
    "Financial Intelligence Platform • Capital Allocation Dashboard"
)