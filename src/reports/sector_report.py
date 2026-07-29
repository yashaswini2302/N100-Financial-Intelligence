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

output_folder = os.path.join(
    BASE_DIR,
    "reports",
    "sectors"
)

os.makedirs(output_folder, exist_ok=True)

for sector in df["sector"].unique():

    sector_df = df[df["sector"] == sector]

    filename = os.path.join(
        output_folder,
        f"{sector}.pdf"
    )

    doc = SimpleDocTemplate(filename)

    story = []

    story.append(
        Paragraph(
            f"<b>{sector} Sector Report</b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            f"Companies : {len(sector_df)}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Average ROE : {sector_df['roe'].mean():.2f}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Average ROA : {sector_df['roa'].mean():.2f}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Average PE Ratio : {sector_df['pe_ratio'].mean():.2f}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            "<br/><b>Companies</b>",
            styles["Heading2"]
        )
    )

    for company in sector_df["company_name"]:
        story.append(
            Paragraph(
                company,
                styles["Normal"]
            )
        )

    doc.build(story)

print("✓ Sector reports generated.")