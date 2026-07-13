import sqlite3

DB_PATH = "data/db/nifty100.db"
OUTPUT = "reports/query_results.txt"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

queries = [
    (
        "Total Companies",
        "SELECT COUNT(*) FROM companies;"
    ),

    (
        "Companies by Sector",
        """
        SELECT sector, COUNT(*)
        FROM companies
        GROUP BY sector;
        """
    ),

    (
        "Top Market Cap Companies",
        """
        SELECT company_name, market_cap_cr
        FROM companies
        ORDER BY market_cap_cr DESC
        LIMIT 5;
        """
    ),

    (
        "Latest Stock Prices",
        """
        SELECT company_id, date, close
        FROM stock_prices
        ORDER BY date DESC
        LIMIT 5;
        """
    )
]

with open(OUTPUT, "w") as f:
    for title, query in queries:
        f.write(f"\n{title}\n")
        f.write("=" * 40 + "\n")

        cursor.execute(query)

        rows = cursor.fetchall()

        if rows:
            for row in rows:
                f.write(str(row) + "\n")
        else:
            f.write("No data found.\n")

conn.close()

print("query_results.txt generated successfully.")