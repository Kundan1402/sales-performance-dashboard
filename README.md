# Sales Performance Analytics Dashboard

Analysis of 3 years of retail sales data using **Python, SQL, Excel and Power BI**.
The goal: find revenue trends, top products, regional performance and seasonal patterns, and turn them into simple business advice.

## Tools
| Tool | Used for |
|------|----------|
| Python + Pandas | Cleaning data, calculating KPIs |
| NumPy | Making the sample data |
| SQLite + SQL | Querying the data (GROUP BY, window functions) |
| Matplotlib | Charts |
| openpyxl | Writing the Excel summary |
| Power BI | Interactive dashboard (KPI cards, slicers, drill-down) |

## Project structure
```
sales-dashboard/
├── 01_generate_data.py       # makes messy sample data
├── 02_clean_data.py          # cleans data, adds revenue/profit columns
├── 03_sql_analysis.py        # loads data to SQLite, runs sql/queries.sql
├── 04_report_and_charts.py   # charts, Excel summary, business summary
├── sql/queries.sql           # all SQL queries
├── data/raw, data/clean      # input and cleaned data
├── outputs/                  # charts, Excel file, business_summary.md
└── requirements.txt
```

## How to run
```bash
pip install -r requirements.txt
python 01_generate_data.py
python 02_clean_data.py
python 03_sql_analysis.py
python 04_report_and_charts.py
```

## Data cleaning done
- Removed 100 duplicate rows
- Fixed two date formats (YYYY-MM-DD and DD/MM/YYYY)
- Fixed text (`" north "` -> `North`)
- Filled missing region, customer and discount values
- Added revenue, profit, year, month, quarter columns

## Power BI dashboard
Open Power BI Desktop -> Get Data -> Text/CSV -> `data/clean/sales_clean.csv`.

Create a date table (Modeling -> New Table):
```
Date = CALENDARAUTO()
```
Link `Date[Date]` to `sales_clean[order_date]` (Model view).

DAX measures:
```
Total Revenue    = SUM(sales_clean[revenue])
Total Profit     = SUM(sales_clean[profit])
Profit Margin %  = DIVIDE([Total Profit], [Total Revenue])
Revenue LY       = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR('Date'[Date]))
YoY Growth %     = DIVIDE([Total Revenue] - [Revenue LY], [Revenue LY])
```
Visuals: 4 KPI cards, line chart (revenue by month), bar chart (region), bar chart (top products), slicers (Year, Region, Category), drill-down on Year -> Quarter -> Month.

## Key findings
See `outputs/business_summary.md`.
