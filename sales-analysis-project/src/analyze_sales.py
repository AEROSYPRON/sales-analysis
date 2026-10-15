"""Retail sales analysis portfolio project.

Run from the repository root:
    python src/analyze_sales.py
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "sales_data.csv"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["Order_Date"])
    required = {
        "Order_ID", "Order_Date", "Region", "Category", "Product",
        "Quantity", "Unit_Price", "Discount", "Unit_Cost",
        "Revenue", "Cost", "Profit"
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")
    if df.empty:
        raise ValueError("Dataset is empty.")
    return df

def main() -> None:
    df = load_data(DATA_PATH)

    # Basic data-quality checks
    print("=== DATA OVERVIEW ===")
    print(f"Rows: {len(df):,}")
    print(f"Date range: {df['Order_Date'].min().date()} to {df['Order_Date'].max().date()}")
    print(f"Duplicate order IDs: {df['Order_ID'].duplicated().sum()}")
    print(f"Missing values: {int(df.isna().sum().sum())}")

    # KPI summary
    total_revenue = df["Revenue"].sum()
    total_cost = df["Cost"].sum()
    total_profit = df["Profit"].sum()
    profit_margin = (total_profit / total_revenue * 100) if total_revenue else 0
    total_units = df["Quantity"].sum()
    average_order_line_revenue = df["Revenue"].mean()

    print("\n=== KEY PERFORMANCE INDICATORS ===")
    print(f"Total revenue:             ${total_revenue:,.2f}")
    print(f"Total cost:                ${total_cost:,.2f}")
    print(f"Total profit:              ${total_profit:,.2f}")
    print(f"Overall profit margin:     {profit_margin:.2f}%")
    print(f"Units sold:                {total_units:,}")
    print(f"Average line revenue:      ${average_order_line_revenue:,.2f}")

    # Monthly trends
    monthly = (
        df.assign(Month=df["Order_Date"].dt.to_period("M").dt.to_timestamp())
          .groupby("Month", as_index=False)
          .agg(Revenue=("Revenue", "sum"), Profit=("Profit", "sum"), Orders=("Order_ID", "count"))
          .sort_values("Month")
    )
    monthly.to_csv(OUTPUT_DIR / "monthly_summary.csv", index=False)
    best_month = monthly.loc[monthly["Revenue"].idxmax()]
    print("\n=== MONTHLY PERFORMANCE ===")
    print(monthly.to_string(index=False, formatters={"Revenue": "{:,.2f}".format, "Profit": "{:,.2f}".format}))
    print(f"Highest-revenue month: {best_month['Month'].strftime('%B %Y')} (${best_month['Revenue']:,.2f})")

    # Region and category summaries
    region_summary = df.groupby("Region", as_index=False).agg(
        Revenue=("Revenue", "sum"), Profit=("Profit", "sum"), Units=("Quantity", "sum")
    ).sort_values("Revenue", ascending=False)
    category_summary = df.groupby("Category", as_index=False).agg(
        Revenue=("Revenue", "sum"), Profit=("Profit", "sum"), Cost=("Cost", "sum")
    )
    category_summary["Profit_Margin_Pct"] = category_summary["Profit"] / category_summary["Revenue"] * 100
    region_summary.to_csv(OUTPUT_DIR / "region_summary.csv", index=False)
    category_summary.to_csv(OUTPUT_DIR / "category_summary.csv", index=False)

    print("\n=== REVENUE BY REGION ===")
    print(region_summary.to_string(index=False, formatters={"Revenue": "{:,.2f}".format, "Profit": "{:,.2f}".format}))
    print("\n=== CATEGORY PERFORMANCE ===")
    print(category_summary.sort_values("Profit", ascending=False).to_string(
        index=False, formatters={"Revenue": "{:,.2f}".format, "Profit": "{:,.2f}".format, "Cost": "{:,.2f}".format, "Profit_Margin_Pct": "{:.2f}%".format}
    ))

    # Product ranking
    product_summary = df.groupby("Product", as_index=False).agg(
        Revenue=("Revenue", "sum"), Profit=("Profit", "sum"), Units=("Quantity", "sum")
    ).sort_values("Revenue", ascending=False)
    product_summary.to_csv(OUTPUT_DIR / "product_summary.csv", index=False)
    print("\n=== TOP 10 PRODUCTS BY REVENUE ===")
    print(product_summary.head(10).to_string(index=False, formatters={"Revenue": "{:,.2f}".format, "Profit": "{:,.2f}".format}))

    # Discount analysis
    df["Discount_Band"] = pd.cut(
        df["Discount"], bins=[-0.001, 0, 0.05, 0.10, 0.15, 0.20],
        labels=["No discount", "Up to 5%", "5–10%", "10–15%", "15–20%"],
        include_lowest=True
    )
    discount_summary = df.groupby("Discount_Band", observed=False, as_index=False).agg(
        Revenue=("Revenue", "sum"), Profit=("Profit", "sum"), Average_Discount=("Discount", "mean")
    )
    discount_summary["Profit_Margin_Pct"] = discount_summary["Profit"] / discount_summary["Revenue"] * 100
    discount_summary.to_csv(OUTPUT_DIR / "discount_summary.csv", index=False)

    # Charts
    plt.figure(figsize=(10, 5))
    plt.plot(monthly["Month"], monthly["Revenue"], marker="o")
    plt.title("Monthly Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "monthly_revenue.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.bar(region_summary["Region"], region_summary["Revenue"])
    plt.title("Revenue by Region")
    plt.xlabel("Region")
    plt.ylabel("Revenue ($)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "revenue_by_region.png", dpi=160)
    plt.close()

    category_plot = category_summary.sort_values("Profit", ascending=False)
    plt.figure(figsize=(9, 5))
    plt.bar(category_plot["Category"], category_plot["Profit"])
    plt.title("Profit by Product Category")
    plt.xlabel("Category")
    plt.ylabel("Profit ($)")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "profit_by_category.png", dpi=160)
    plt.close()

    top_products = product_summary.head(10).sort_values("Revenue")
    plt.figure(figsize=(9, 6))
    plt.barh(top_products["Product"], top_products["Revenue"])
    plt.title("Top 10 Products by Revenue")
    plt.xlabel("Revenue ($)")
    plt.ylabel("Product")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "top_products.png", dpi=160)
    plt.close()

    print(f"\nAnalysis complete. Tables and charts saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
