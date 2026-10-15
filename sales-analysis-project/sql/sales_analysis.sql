-- Retail Sales Analysis
-- Table name assumed: sales_data
-- Load data/sales_data.csv into your SQL database first.

-- 1. Overall KPIs
SELECT
    SUM(Revenue) AS total_revenue,
    SUM(Cost) AS total_cost,
    SUM(Profit) AS total_profit,
    ROUND(100.0 * SUM(Profit) / NULLIF(SUM(Revenue), 0), 2) AS profit_margin_pct,
    SUM(Quantity) AS units_sold
FROM sales_data;

-- 2. Revenue and profit by region
SELECT Region, SUM(Revenue) AS revenue, SUM(Profit) AS profit
FROM sales_data
GROUP BY Region
ORDER BY revenue DESC;

-- 3. Category profitability
SELECT
    Category,
    SUM(Revenue) AS revenue,
    SUM(Profit) AS profit,
    ROUND(100.0 * SUM(Profit) / NULLIF(SUM(Revenue), 0), 2) AS profit_margin_pct
FROM sales_data
GROUP BY Category
ORDER BY profit DESC;

-- 4. Top 10 products by revenue
SELECT Product, SUM(Revenue) AS revenue, SUM(Profit) AS profit, SUM(Quantity) AS units_sold
FROM sales_data
GROUP BY Product
ORDER BY revenue DESC
LIMIT 10;

-- 5. Monthly revenue and profit (SQLite/PostgreSQL-style date formatting)
SELECT
    SUBSTR(Order_Date, 1, 7) AS order_month,
    SUM(Revenue) AS revenue,
    SUM(Profit) AS profit,
    COUNT(*) AS order_lines
FROM sales_data
GROUP BY SUBSTR(Order_Date, 1, 7)
ORDER BY order_month;

-- 6. Discount impact
SELECT
    Discount,
    COUNT(*) AS order_lines,
    SUM(Revenue) AS revenue,
    SUM(Profit) AS profit,
    ROUND(100.0 * SUM(Profit) / NULLIF(SUM(Revenue), 0), 2) AS profit_margin_pct
FROM sales_data
GROUP BY Discount
ORDER BY Discount;
