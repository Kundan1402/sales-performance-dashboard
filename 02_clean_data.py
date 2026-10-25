"""
STEP 2: Clean the raw data with Pandas.

We fix: duplicates, mixed date formats, inconsistent text, missing values.
Then we add new columns (revenue, profit, year, month...) that reporting needs.
"""
import pandas as pd
from pathlib import Path

raw = pd.read_csv("data/raw/sales_raw.csv")

# ---- 1. LOOK at the problems first (always do this!) ----
print("Rows before cleaning :", len(raw))
print("Duplicate rows       :", raw.duplicated().sum())
print("Missing values per column:")
print(raw.isna().sum()[raw.isna().sum() > 0], "\n")

df = raw.copy()

# ---- 2. Remove duplicates ----
df = df.drop_duplicates()

# ---- 3. Fix dates (two formats in one column) ----
# Try format 1. Rows that do not match become NaT (empty). Then try format 2 on those.
d1 = pd.to_datetime(df["order_date"], format="%Y-%m-%d", errors="coerce")
d2 = pd.to_datetime(df["order_date"], format="%d/%m/%Y", errors="coerce")
df["order_date"] = d1.fillna(d2)
df = df.dropna(subset=["order_date"])        # drop rows whose date we cannot read

# ---- 4. Fix text: remove spaces, make "north" -> "North" ----
df["region"] = df["region"].str.strip().str.title()

# ---- 5. Fill missing values ----
df["region"] = df["region"].fillna("Unknown")
df["customer_id"] = df["customer_id"].fillna("UNKNOWN")
df["discount"] = df["discount"].fillna(0)    # no discount info = assume no discount

# ---- 6. Create new columns (feature engineering) ----
df["revenue"] = (df["quantity"] * df["unit_price"] * (1 - df["discount"])).round(2)
df["total_cost"] = (df["quantity"] * df["cost"]).round(2)
df["profit"] = (df["revenue"] - df["total_cost"]).round(2)
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["month_name"] = df["order_date"].dt.strftime("%b")
df["quarter"] = df["order_date"].dt.quarter

# ---- 7. Save ----
Path("data/clean").mkdir(parents=True, exist_ok=True)
df.to_csv("data/clean/sales_clean.csv", index=False)
print("Rows after cleaning  :", len(df))
print("Saved: data/clean/sales_clean.csv")
