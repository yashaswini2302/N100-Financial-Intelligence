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
    page_title="Peer Comparison",
    page_icon="📊",
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

st.title("📊 Peer Comparison")

st.caption(
    "Compare multiple companies across important financial metrics."
)

st.divider()

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

st.sidebar.header("Peer Selection")

sector = st.sidebar.selectbox(
    "Filter by Sector",
    ["All"] + sorted(df["sector"].unique().tolist())
)

if sector != "All":
    available = (
        df[df["sector"] == sector]
        .sort_values("company_name")
    )
else:
    available = df.sort_values("company_name")

selected = st.sidebar.multiselect(
    "Choose Companies",
    available["company_name"],
    default=available["company_name"].head(3).tolist()
)

peer_df = available[
    available["company_name"].isin(selected)
].copy()

# ----------------------------------------------------
# VALIDATION
# ----------------------------------------------------

if len(peer_df) < 2:

    st.warning(
        "Please select at least two companies for comparison."
    )

    st.stop()

# ----------------------------------------------------
# KPI CARDS
# ----------------------------------------------------

st.subheader("Comparison Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Companies",
    len(peer_df)
)

c2.metric(
    "Highest ROE",
    f"{peer_df['return_on_equity_pct'].max():.2f}%"
)

c3.metric(
    "Highest Margin",
    f"{peer_df['net_profit_margin_pct'].max():.2f}%"
)

c4.metric(
    "Best Quality Score",
    peer_df["quality_score"].max()
)

st.divider()

# ----------------------------------------------------
# COMPARISON TABLE
# ----------------------------------------------------

st.subheader("Financial Comparison")

comparison = peer_df[
    [
        "company_name",
        "sector",
        "market_cap_cr",
        "return_on_equity_pct",
        "return_on_assets_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "quality_score"
    ]
].copy()

comparison.columns = [
    "Company",
    "Sector",
    "Market Cap (Cr)",
    "ROE (%)",
    "ROA (%)",
    "Net Profit Margin (%)",
    "Debt / Equity",
    "Revenue CAGR (%)",
    "PAT CAGR (%)",
    "Quality Score"
]

st.dataframe(
    comparison,
    use_container_width=True,
    hide_index=True
)

st.divider()
# ----------------------------------------------------
# RADAR CHART
# ----------------------------------------------------

st.subheader("Performance Radar")

radar_metrics = [
    "return_on_equity_pct",
    "return_on_assets_pct",
    "net_profit_margin_pct",
    "revenue_cagr_5yr",
    "pat_cagr_5yr"
]

radar_labels = [
    "ROE",
    "ROA",
    "Margin",
    "Revenue CAGR",
    "PAT CAGR"
]

fig = go.Figure()

for _, row in peer_df.iterrows():

    fig.add_trace(
        go.Scatterpolar(
            r=[
                row["return_on_equity_pct"],
                row["return_on_assets_pct"],
                row["net_profit_margin_pct"],
                row["revenue_cagr_5yr"],
                row["pat_cagr_5yr"]
            ],
            theta=radar_labels,
            fill="toself",
            name=row["company_name"]
        )
    )

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True
        )
    ),
    height=600,
    showlegend=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ----------------------------------------------------
# ROE COMPARISON
# ----------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("Return on Equity")

    fig1 = px.bar(
        peer_df.sort_values(
            "return_on_equity_pct",
            ascending=False
        ),
        x="company_name",
        y="return_on_equity_pct",
        color="company_name",
        text="return_on_equity_pct"
    )

    fig1.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig1.update_layout(
        height=450,
        showlegend=False,
        xaxis_title="",
        yaxis_title="ROE (%)"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with right:

    st.subheader("Net Profit Margin")

    fig2 = px.bar(
        peer_df.sort_values(
            "net_profit_margin_pct",
            ascending=False
        ),
        x="company_name",
        y="net_profit_margin_pct",
        color="company_name",
        text="net_profit_margin_pct"
    )

    fig2.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig2.update_layout(
        height=450,
        showlegend=False,
        xaxis_title="",
        yaxis_title="Margin (%)"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.divider()

# ----------------------------------------------------
# DEBT & GROWTH
# ----------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("Debt to Equity")

    fig3 = px.bar(
        peer_df.sort_values(
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

with right:

    st.subheader("Revenue CAGR")

    fig4 = px.bar(
        peer_df.sort_values(
            "revenue_cagr_5yr",
            ascending=False
        ),
        x="company_name",
        y="revenue_cagr_5yr",
        color="company_name",
        text="revenue_cagr_5yr"
    )

    fig4.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig4.update_layout(
        height=450,
        showlegend=False,
        xaxis_title="",
        yaxis_title="Revenue CAGR (%)"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

st.divider()
# ----------------------------------------------------
# OVERALL SCORECARD
# ----------------------------------------------------

st.subheader("🏆 Overall Peer Ranking")

score_df = peer_df.copy()
score_df = score_df.fillna(0)

score_df["Overall Score"] = (
    score_df["return_on_equity_pct"] * 0.30 +
    score_df["return_on_assets_pct"] * 0.15 +
    score_df["net_profit_margin_pct"] * 0.20 +
    score_df["revenue_cagr_5yr"] * 0.15 +
    score_df["pat_cagr_5yr"] * 0.10 +
    score_df["quality_score"] * 2 -
    score_df["debt_to_equity"] * 10
)

score_df = score_df.sort_values(
    "Overall Score",
    ascending=False
).reset_index(drop=True)

score_df["Rank"] = score_df.index + 1

ranking = score_df[
    [
        "Rank",
        "company_name",
        "Overall Score",
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "quality_score"
    ]
].copy()

ranking.columns = [
    "Rank",
    "Company",
    "Overall Score",
    "ROE (%)",
    "Margin (%)",
    "Debt / Equity",
    "Quality"
]

st.dataframe(
    ranking,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ----------------------------------------------------
# WINNER
# ----------------------------------------------------

winner = score_df.iloc[0]

st.success(
    f"""
🏆 **Best Performing Company**

**{winner['company_name']}**

Overall Score : **{winner['Overall Score']:.2f}**

ROE : **{winner['return_on_equity_pct']:.2f}%**

Net Profit Margin : **{winner['net_profit_margin_pct']:.2f}%**

Revenue CAGR : **{winner['revenue_cagr_5yr']:.2f}%**

Quality Score : **{winner['quality_score']}**
"""
)

st.divider()

# ----------------------------------------------------
# DOWNLOADS
# ----------------------------------------------------

st.subheader("Download Comparison")

csv = ranking.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📄 Download CSV",
    data=csv,
    file_name="peer_comparison.csv",
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
        sheet_name="Peer Comparison"
    )

st.download_button(
    label="📊 Download Excel",
    data=excel_buffer.getvalue(),
    file_name="peer_comparison.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.divider()

# ----------------------------------------------------
# KEY INSIGHTS
# ----------------------------------------------------

st.subheader("Key Insights")

highest_roe = peer_df.loc[
    peer_df["return_on_equity_pct"].idxmax(),
    "company_name"
]

highest_margin = peer_df.loc[
    peer_df["net_profit_margin_pct"].idxmax(),
    "company_name"
]

lowest_debt = peer_df.loc[
    peer_df["debt_to_equity"].idxmin(),
    "company_name"
]

fastest_growth = peer_df.loc[
    peer_df["revenue_cagr_5yr"].idxmax(),
    "company_name"
]

st.info(
    f"""
• 🥇 Highest ROE : **{highest_roe}**

• 💰 Highest Net Profit Margin : **{highest_margin}**

• 🛡 Lowest Debt / Equity : **{lowest_debt}**

• 📈 Highest Revenue CAGR : **{fastest_growth}**
"""
)

st.divider()

# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------

st.caption(
    "Financial Intelligence Platform • Peer Comparison Dashboard"
)
