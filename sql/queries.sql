-- Each query starts with a name line. Python reads this file and runs every query.
-- Table name: sales

-- name: revenue_by_year
WITH yearly AS (
    SELECT year,
           ROUND(SUM(revenue), 2) AS revenue,
           ROUND(SUM(profit), 2)  AS profit
    FROM sales
    GROUP BY year
)
SELECT year,
       revenue,
       profit,
       ROUND(100.0 * profit / revenue, 2) AS profit_margin_pct,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY year))
             / LAG(revenue) OVER (ORDER BY year), 2) AS yoy_growth_pct
FROM yearly
ORDER BY year;

-- name: top_5_products
SELECT product,
       category,
       ROUND(SUM(revenue), 2) AS revenue,
       ROUND(SUM(profit), 2)  AS profit,
       SUM(quantity)          AS units_sold
FROM sales
GROUP BY product, category
ORDER BY revenue DESC
LIMIT 5;

-- name: region_performance
SELECT region,
       COUNT(DISTINCT order_id)           AS orders,
       ROUND(SUM(revenue), 2)             AS revenue,
       ROUND(100.0 * SUM(profit) / SUM(revenue), 2) AS profit_margin_pct
FROM sales
GROUP BY region
ORDER BY revenue DESC;

-- name: category_performance
SELECT category,
       ROUND(SUM(revenue), 2) AS revenue,
       ROUND(100.0 * SUM(profit) / SUM(revenue), 2) AS profit_margin_pct
FROM sales
GROUP BY category
ORDER BY revenue DESC;

-- name: seasonality_by_month
SELECT month,
       month_name,
       ROUND(SUM(revenue), 2) AS revenue
FROM sales
GROUP BY month, month_name
ORDER BY month;
