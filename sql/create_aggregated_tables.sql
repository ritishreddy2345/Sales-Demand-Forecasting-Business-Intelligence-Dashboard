CREATE OR REPLACE TABLE `vigilant-sunup-498715-e4.sales_forecasting_db.daily_sales_aggregated` AS
SELECT
  DATE(transaction_date) AS sales_date,
  SUM(total_revenue) AS total_revenue,
  SUM(quantity_sold) AS total_quantity_sold,
  COUNT(*) AS total_orders
FROM `vigilant-sunup-498715-e4.sales_forecasting_db.transactions`
GROUP BY sales_date
ORDER BY sales_date;


CREATE OR REPLACE TABLE `vigilant-sunup-498715-e4.sales_forecasting_db.monthly_sales_aggregated` AS
SELECT
  DATE_TRUNC(DATE(transaction_date), MONTH) AS sales_month,
  SUM(total_revenue) AS total_revenue,
  SUM(quantity_sold) AS total_quantity_sold,
  COUNT(*) AS total_orders
FROM `vigilant-sunup-498715-e4.sales_forecasting_db.transactions`
GROUP BY sales_month
ORDER BY sales_month;


CREATE OR REPLACE TABLE `vigilant-sunup-498715-e4.sales_forecasting_db.category_sales_aggregated` AS
SELECT
  product_category,
  SUM(total_revenue) AS total_revenue,
  SUM(quantity_sold) AS total_quantity_sold,
  COUNT(*) AS total_orders
FROM `vigilant-sunup-498715-e4.sales_forecasting_db.transactions`
GROUP BY product_category
ORDER BY total_revenue DESC;