import os
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

companies = pd.read_excel(
    os.path.join(BASE_DIR, "data", "raw", "companies.xlsx")
)

financial = pd.read_excel(
    os.path.join(BASE_DIR, "data", "raw", "financial_ratios.xlsx")
)

df = companies.merge(
    financial,
    on="company_id",
    how="left"
)

os.makedirs(
    os.path.join(BASE_DIR, "reports", "tearsheets"),
    exist_ok=True
)

styles = getSampleStyleSheet()

for _, row in df.iterrows():

    filename = os.path.join(
        BASE_DIR,
        "reports",
        "tearsheets",
        f"{row['company_name']}.pdf"
    )

    doc = SimpleDocTemplate(filename)

    story = []

    story.append(Paragraph(f"<b>{row['company_name']}</b>", styles["Title"]))
    story.append(Paragraph(f"Ticker : {row['ticker_x']}", styles["Normal"]))
    story.append(Paragraph(f"Sector : {row['sector']}", styles["Normal"]))
    story.append(Paragraph(f"Industry : {row['industry']}", styles["Normal"]))
    story.append(Paragraph(f"Market Cap : {row['market_cap_cr']} Cr", styles["Normal"]))
    story.append(Paragraph(f"Founded : {row['founded_year']}", styles["Normal"]))
    story.append(Paragraph(f"Headquarters : {row['headquarters']}", styles["Normal"]))

    story.append(Paragraph("<br/><b>Financial Ratios</b>", styles["Heading2"]))

    story.append(Paragraph(f"PE Ratio : {row['pe_ratio']}", styles["Normal"]))
    story.append(Paragraph(f"ROE : {row['roe']}%", styles["Normal"]))
    story.append(Paragraph(f"ROA : {row['roa']}%", styles["Normal"]))
    story.append(Paragraph(f"Debt / Equity : {row['debt_equity']}", styles["Normal"]))
    story.append(Paragraph(f"Current Ratio : {row['current_ratio']}", styles["Normal"]))
    story.append(Paragraph(f"Financial Year : {row['financial_year']}", styles["Normal"]))

    doc.build(story)

print("✓ Company tearsheets generated successfully.")