CREATE TABLE IF NOT EXISTS companies (
    company_id INTEGER PRIMARY KEY,
    company_name TEXT,
    ticker TEXT,
    sector TEXT,
    industry TEXT,
    market_cap_cr REAL,
    founded_year INTEGER,
    headquarters TEXT
);

CREATE TABLE IF NOT EXISTS balancesheet (
    company_id INTEGER,
    year INTEGER,
    total_assets REAL,
    total_liabilities REAL,
    equity REAL
);

CREATE TABLE IF NOT EXISTS profitandloss (
    company_id INTEGER,
    year INTEGER,
    revenue REAL,
    net_profit REAL,
    eps REAL
);

CREATE TABLE IF NOT EXISTS cashflow (
    company_id INTEGER,
    year INTEGER,
    operating_cashflow REAL,
    investing_cashflow REAL,
    financing_cashflow REAL
);

CREATE TABLE IF NOT EXISTS analysis (
    company_id INTEGER,
    score REAL,
    recommendation TEXT
);

CREATE TABLE IF NOT EXISTS financial_ratios (
    company_id INTEGER,
    year INTEGER,
    roe REAL,
    roa REAL,
    debt_to_equity REAL
);

CREATE TABLE IF NOT EXISTS sectors (
    sector TEXT PRIMARY KEY,
    description TEXT
);

CREATE TABLE IF NOT EXISTS peer_groups (
    company_id INTEGER,
    peer_company TEXT
);

CREATE TABLE IF NOT EXISTS prosandcons (
    company_id INTEGER,
    pros TEXT,
    cons TEXT
);

CREATE TABLE IF NOT EXISTS documents (
    company_id INTEGER,
    document_name TEXT,
    document_type TEXT
);

CREATE TABLE IF NOT EXISTS stock_prices (
    company_id INTEGER,
    trade_date TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER
);

CREATE TABLE IF NOT EXISTS load_audit (
    file_name TEXT,
    rows_loaded INTEGER,
    load_time TEXT
);