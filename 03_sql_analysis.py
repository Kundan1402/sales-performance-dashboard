"""
STEP 3: Load the clean data into a SQL database and run SQL queries.

We use SQLite. It comes built into Python, so you install nothing.
The database is just one file: sales.db
"""
import sqlite3
import pandas as pd
from pathlib import Path

# ---- 1. Load clean CSV into a SQLite table called "sales" ----
df = pd.read_csv("data/clean/sales_clean.csv")
conn = sqlite3.connect("sales.db")              # creates sales.db if it does not exist
df.to_sql("sales", conn, if_exists="replace", index=False)
print(f"Loaded {len(df)} rows into table 'sales'\n")

# ---- 2. Read queries.sql and run each query ----
text = Path("sql/queries.sql").read_text()
blocks = text.split("-- name:")[1:]             # one block per query

Path("outputs/sql_results").mkdir(parents=True, exist_ok=True)
for block in blocks:
    name, query = block.split("\n", 1)
    name = name.strip()
    result = pd.read_sql_query(query, conn)     # run SQL, get a DataFrame back
    print(f"=== {name} ===")
    print(result.to_string(index=False), "\n")
    result.to_csv(f"outputs/sql_results/{name}.csv", index=False)

conn.close()
print("SQL results saved in outputs/sql_results/")
