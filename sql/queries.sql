-- 1. Total Companies
SELECT COUNT(*) AS total_companies
FROM companies;

-- 2. Companies by Sector
SELECT sector, COUNT(*) AS companies
FROM companies
GROUP BY sector
ORDER BY companies DESC;

-- 3. Highest Market Cap Companies
SELECT company_name, market_cap_cr
FROM companies
ORDER BY market_cap_cr DESC
LIMIT 10;

-- 4. Latest Stock Prices
SELECT company_id, date, close
FROM stock_prices
ORDER BY date DESC
LIMIT 10;

-- 5. Companies Founded Before 2000
SELECT company_name, founded_year
FROM companies
WHERE founded_year < 2000
ORDER BY founded_year;

-- 6. Financial Ratios
SELECT company_id, year, roe, roa
FROM financial_ratios
LIMIT 10;

-- 7. Profit Leaders
SELECT company_id, year, net_profit
FROM profitandloss
ORDER BY net_profit DESC
LIMIT 10;

-- 8. Cash Flow
SELECT company_id, year, operating_cashflow
FROM cashflow
LIMIT 10;

-- 9. Audit Summary
SELECT *
FROM load_audit;

-- 10. Sector List
SELECT *
FROM sectors;