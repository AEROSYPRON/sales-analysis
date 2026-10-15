# Sales Data Analysis Project

A beginner-to-intermediate **Python, Pandas, SQL, and data visualization** project that analyzes retail sales performance.

## Project goals
- Measure total revenue, cost, profit, and profit margin.
- Find monthly sales trends.
- Compare performance by region and product category.
- Identify top products and products with weaker profit.
- Explore the relationship between discounts and profitability.

## Dataset
`data/sales_data.csv` is included, so you can run the project immediately without downloading anything.

This is a **synthetic practice dataset generated for this portfolio project**, not real company data. It contains 1,200 order-line records covering 2024. Each row represents one order line.

Important columns:
- `Order_ID`, `Order_Date`: order identifier and date
- `Region`, `Category`, `Product`: sales dimensions
- `Quantity`, `Unit_Price`, `Discount`: units, listed price, and discount rate
- `Unit_Cost`, `Revenue`, `Cost`, `Profit`: financial metrics

Revenue is calculated as `Unit_Price × Quantity × (1 - Discount)`. Profit is `Revenue - Cost`.

## Tech stack
- Python
- Pandas and NumPy
- Matplotlib
- SQL (queries provided)

## Project structure
```text
sales-analysis-project/
├── data/
│   └── sales_data.csv
├── outputs/
│   ├── monthly_revenue.png
│   ├── revenue_by_region.png
│   ├── profit_by_category.png
│   └── top_products.png
├── sql/
│   └── sales_analysis.sql
├── src/
│   └── analyze_sales.py
├── requirements.txt
└── README.md
```

## Run it locally
1. Install Python 3.10 or newer.
2. Open a terminal in the project folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the analysis:
   ```bash
   python src/analyze_sales.py
   ```

The script prints summary metrics and saves charts into `outputs/`.

## SQL
Open `sql/sales_analysis.sql` to review equivalent analysis queries. The SQL is written in broadly compatible SQL style; minor date-function changes may be needed for your database.

## Key questions to explore
1. Which month generated the highest revenue?
2. Which region generated the most revenue and profit?
3. Which category had the highest profit margin?
4. Which products generated the most revenue?
5. Do higher discounts appear alongside lower profit margins?

## Important note
Because this dataset is synthetic, describe this as a **portfolio/practice project** and do not present the results as findings from a real business.
