"""
STEP 4: Pandas analysis + charts + Excel summary + business summary.
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")                           # lets charts save to files without a window
import matplotlib.pyplot as plt
from pathlib import Path

df = pd.read_csv("data/clean/sales_clean.csv", parse_dates=["order_date"])
Path("outputs/charts").mkdir(parents=True, exist_ok=True)

# ---------- KPIs ----------
total_revenue = df["revenue"].sum()
total_profit = df["profit"].sum()
margin = 100 * total_profit / total_revenue
orders = df["order_id"].nunique()
avg_order = total_revenue / orders

# ---------- Summary tables ----------
by_year = df.groupby("year").agg(revenue=("revenue", "sum"), profit=("profit", "sum")).round(2)
by_year["profit_margin_pct"] = (100 * by_year["profit"] / by_year["revenue"]).round(2)
by_year["yoy_growth_pct"] = (by_year["revenue"].pct_change() * 100).round(2)

by_region = (df.groupby("region").agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
             .round(2).sort_values("revenue", ascending=False))
by_region["profit_margin_pct"] = (100 * by_region["profit"] / by_region["revenue"]).round(2)

top_products = (df.groupby("product").agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
                .round(2).sort_values("revenue", ascending=False).head(5))

monthly = df.groupby("month_name", as_index=False).agg(revenue=("revenue", "sum"), month=("month", "first"))
monthly = monthly.sort_values("month")

kpis = pd.DataFrame({
    "KPI": ["Total Revenue", "Total Profit", "Profit Margin %", "Total Orders", "Avg Order Value"],
    "Value": [round(total_revenue, 2), round(total_profit, 2), round(margin, 2), orders, round(avg_order, 2)],
})

# ---------- Charts ----------
def save_bar(series, title, filename, xlabel=""):
    ax = series.plot(kind="bar", figsize=(7, 4), color="#2a6fdb")
    ax.set_title(title); ax.set_xlabel(xlabel); ax.set_ylabel("Revenue")
    plt.xticks(rotation=0); plt.tight_layout()
    plt.savefig(f"outputs/charts/{filename}", dpi=120); plt.close()

save_bar(by_year["revenue"], "Revenue by Year", "revenue_by_year.png", "Year")
save_bar(by_region["revenue"], "Revenue by Region", "revenue_by_region.png", "Region")
save_bar(top_products["revenue"], "Top 5 Products by Revenue", "top_products.png", "Product")

plt.figure(figsize=(8, 4))
plt.plot(monthly["month_name"], monthly["revenue"], marker="o", color="#2a6fdb")
plt.title("Seasonality: Revenue by Month (all years)")
plt.ylabel("Revenue"); plt.tight_layout()
plt.savefig("outputs/charts/seasonality.png", dpi=120); plt.close()

# ---------- Excel file (each table on its own sheet) ----------
with pd.ExcelWriter("outputs/sales_summary.xlsx") as writer:
    kpis.to_excel(writer, sheet_name="KPIs", index=False)
    by_year.to_excel(writer, sheet_name="By Year")
    by_region.to_excel(writer, sheet_name="By Region")
    top_products.to_excel(writer, sheet_name="Top Products")
    monthly.to_excel(writer, sheet_name="Monthly", index=False)

# ---------- Business summary in plain words ----------
best_region = by_region.index[0]
best_product = top_products.index[0]
peak_month = monthly.loc[monthly["revenue"].idxmax(), "month_name"]
low_month = monthly.loc[monthly["revenue"].idxmin(), "month_name"]
best_margin_region = by_region["profit_margin_pct"].idxmax()
last_yoy = by_year["yoy_growth_pct"].iloc[-1]

summary = f"""# Business Summary

**Overall:** Revenue is {total_revenue:,.0f} with a profit margin of {margin:.1f}% across {orders:,} orders.

## Key insights
1. Revenue grew {last_yoy:.1f}% in the latest year compared with the year before.
2. **{best_region}** is the top region by revenue. **{best_margin_region}** has the best profit margin.
3. **{best_product}** is the best-selling product by revenue.
4. Sales peak in **{peak_month}** and are lowest in **{low_month}**.

## Recommendations
- Stock more inventory and run campaigns before **{peak_month}**, when demand is highest.
- Push marketing in regions with lower revenue to grow them.
"""
Path("outputs/business_summary.md").write_text(summary)

print(kpis.to_string(index=False))
print("\nBy year:\n", by_year)
print("\nSaved: outputs/sales_summary.xlsx, outputs/business_summary.md, outputs/charts/*.png")
