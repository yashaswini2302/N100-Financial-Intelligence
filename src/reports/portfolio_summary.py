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

styles = getSampleStyleSheet()

os.makedirs(
    os.path.join(BASE_DIR, "reports"),
    exist_ok=True
)

filename = os.path.join(
    BASE_DIR,
    "reports",
    "portfolio_summary.pdf"
)

doc = SimpleDocTemplate(filename)

story = []

story.append(Paragraph("<b>Portfolio Summary Report</b>", styles["Title"]))

story.append(Paragraph(f"Total Companies : {len(df)}", styles["Normal"]))
story.append(Paragraph(f"Total Sectors : {df['sector'].nunique()}", styles["Normal"]))
story.append(Paragraph(f"Average PE Ratio : {df['pe_ratio'].mean():.2f}", styles["Normal"]))
story.append(Paragraph(f"Average ROE : {df['roe'].mean():.2f}", styles["Normal"]))
story.append(Paragraph(f"Average ROA : {df['roa'].mean():.2f}", styles["Normal"]))
story.append(Paragraph(f"Average Debt/Equity : {df['debt_equity'].mean():.2f}", styles["Normal"]))
story.append(Paragraph(f"Average Current Ratio : {df['current_ratio'].mean():.2f}", styles["Normal"]))

story.append(Paragraph("<br/><b>Companies Included</b>", styles["Heading2"]))

for company in sorted(df["company_name"]):
    story.append(Paragraph(company, styles["Normal"]))

doc.build(story)

print("✓ Portfolio summary generated successfully.")