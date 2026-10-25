"""
STEP 1: Create a fake (but realistic) messy sales dataset.

Why? Real company data is private. So we make our own data that has the
same problems real data has: missing values, duplicates, mixed date formats,
and inconsistent text. Later we will clean it.

(If you prefer real data, download the "Superstore" dataset from Kaggle
and skip this step. You will need to rename columns to match our names.)
"""
import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)          # same random numbers every run, so results repeat
N = 5000                    # number of orders

# ---- Products: category -> {product: price} ----
catalog = {
    "Technology": {"Laptop": 900, "Phone": 600, "Headphones": 80, "Monitor": 250},
    "Furniture": {"Chair": 150, "Desk": 300, "Bookshelf": 180},
    "Office Supplies": {"Notebook": 5, "Pen Pack": 8, "Printer Paper": 20, "Stapler": 12},
}
items = [(cat, prod, price) for cat, prods in catalog.items() for prod, price in prods.items()]

# ---- Dates: more sales in Nov/Dec (seasonality) and growth every year ----
all_days = pd.date_range("2022-01-01", "2024-12-31")
weights = np.ones(len(all_days))
weights[all_days.month.isin([11, 12])] *= 2      # festive season = 2x orders
weights[all_days.year == 2023] *= 1.2            # 2023 grows 20%
weights[all_days.year == 2024] *= 1.4            # 2024 grows more
weights = weights / weights.sum()
order_dates = np.random.choice(all_days, size=N, p=weights)

# ---- Build the table ----
pick = np.random.randint(0, len(items), N)
df = pd.DataFrame({
    "order_id": [f"ORD{100000 + i}" for i in range(N)],
    "order_date": pd.to_datetime(order_dates),
    "customer_id": [f"C{np.random.randint(1, 801):04d}" for _ in range(N)],
    "region": np.random.choice(["North", "South", "East", "West"], N, p=[0.30, 0.25, 0.25, 0.20]),
    "category": [items[i][0] for i in pick],
    "product": [items[i][1] for i in pick],
    "quantity": np.random.randint(1, 6, N),
    "unit_price": [items[i][2] for i in pick],
    "discount": np.random.choice([0, 0.05, 0.10, 0.20], N, p=[0.5, 0.2, 0.2, 0.1]),
})
# cost per unit is 60% to 80% of the price
df["cost"] = (df["unit_price"] * np.random.uniform(0.6, 0.8, N)).round(2)

# ---- Now make the data MESSY on purpose ----
# 1) Mixed date formats: 90% are 2023-05-17, 10% are 17/05/2023
df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")
mask = np.random.rand(N) < 0.10
as_dates = pd.to_datetime(df.loc[mask, "order_date"])
df.loc[mask, "order_date"] = as_dates.dt.strftime("%d/%m/%Y")

# 2) Inconsistent text: "north", "  North "
m1 = np.random.rand(N) < 0.05
df.loc[m1, "region"] = df.loc[m1, "region"].str.lower()
m2 = np.random.rand(N) < 0.05
df.loc[m2, "region"] = "  " + df.loc[m2, "region"] + " "

# 3) Missing values
for col, frac in [("region", 0.02), ("discount", 0.03), ("customer_id", 0.02)]:
    df.loc[np.random.rand(N) < frac, col] = np.nan

# 4) Duplicate rows (100 rows copied)
df = pd.concat([df, df.sample(100, random_state=1)], ignore_index=True)

Path("data/raw").mkdir(parents=True, exist_ok=True)
df.to_csv("data/raw/sales_raw.csv", index=False)
print(f"Done. Created data/raw/sales_raw.csv with {len(df)} rows.")
