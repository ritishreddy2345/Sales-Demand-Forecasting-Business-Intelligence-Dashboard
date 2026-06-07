"""
PHASE 4: Looker Studio Dashboard Design Blueprint
Comprehensive blueprint for 3-tab interactive KPI dashboard
"""

LOOKER_STUDIO_DASHBOARD_BLUEPRINT = """
================================================================================
                    LOOKER STUDIO DASHBOARD DESIGN BLUEPRINT
                Sales Demand Forecasting & Business Intelligence
================================================================================

PROJECT OVERVIEW:
- Dashboard Name: Sales Demand Forecasting & Business Intelligence Dashboard
- Data Source: Google BigQuery (GCP Project)
- Refresh Schedule: Daily (automated via BigQuery scheduled queries)
- Target Audience: C-Level Executives, Sales Managers, Inventory Managers
- Dashboard Type: 3-tab interactive KPI dashboard
- Performance Target: All queries must complete within 10 seconds

================================================================================
TAB 1: EXECUTIVE REVENUE TRENDS & DEMAND FORECASTING
================================================================================

Purpose:
  Track historical revenue performance, identify trends, and visualize 
  90-day demand forecasts vs. actual for strategic planning

Data Source Tables:
  - transactions (fact table)
  - daily_sales_aggregated (aggregated daily sales by category)
  - demand_forecast (90-day forecast from Prophet/ARIMA)

SECTION 1A: HEADER KPI CARDS (4 Cards in Row)
────────────────────────────────────────────────────────────────────────────────

1. Total Revenue (YTD)
   - Metric Query:
     SELECT ROUND(SUM(total_revenue), 2) as total_revenue_ytd
     FROM transactions
     WHERE EXTRACT(YEAR FROM transaction_date) = EXTRACT(YEAR FROM CURRENT_DATE())
   
   - Dimension: None (Single Value)
   - Format: Currency ($)
   - Color Coding:
     * Green if > 15% growth vs. prior year
     * Yellow if 0-15% growth
     * Red if negative growth
   - Comparison: YoY growth percentage
   - Size: Large card (spanning 2 columns)

2. Average Daily Revenue
   - Metric Query:
     SELECT ROUND(AVG(daily_total), 2) as avg_daily_revenue
     FROM (
       SELECT DATE(transaction_date) as date, SUM(total_revenue) as daily_total
       FROM transactions
       WHERE transaction_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
       GROUP BY date
     )
   
   - Dimension: None (Single Value)
   - Format: Currency ($)
   - Size: Medium card (spanning 1 column)

3. 90-Day Forecast Accuracy
   - Metric Query:
     SELECT ROUND(100 * AVG(accuracy), 2) as forecast_accuracy_pct
     FROM forecast_models_metrics
     WHERE model_type IN ('prophet', 'arima')
       AND DATE(evaluation_date) = CURRENT_DATE()
   
   - Dimension: None (Single Value)
   - Format: Percentage
   - Target: 87%
   - Status Indicator: ✓ (Green) if >= 87%, ✗ (Red) if < 87%
   - Size: Medium card (spanning 1 column)

4. Forecast vs. Actual Gap
   - Metric Query:
     SELECT ROUND(
       100 * ABS(SUM(forecasted) - SUM(actual)) / SUM(actual), 2
     ) as forecast_gap_pct
     FROM (
       SELECT forecasted_revenue as forecasted, actual_revenue as actual
       FROM demand_forecast
       WHERE DATE(forecast_date) <= CURRENT_DATE()
     )
   
   - Dimension: None (Single Value)
   - Format: Percentage
   - Color: Green if < 10%, Yellow if 10-20%, Red if > 20%
   - Size: Medium card (spanning 1 column)

SECTION 1B: TIME-SERIES CHART - HISTORICAL vs. FORECAST
────────────────────────────────────────────────────────────────────────────────

Chart Type: Combo Chart (Line + Bars)
Title: "90-Day Revenue Forecast vs. Historical Actuals"
Height: 400px (spanning full width)

Data Query:
  WITH historical AS (
    SELECT 
      DATE(transaction_date) as date,
      SUM(total_revenue) as actual_revenue,
      'Historical' as data_type
    FROM transactions
    WHERE transaction_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)
    GROUP BY date
  ),
  forecast_data AS (
    SELECT 
      forecast_date as date,
      forecasted_revenue,
      'Forecasted' as data_type
    FROM demand_forecast
    WHERE forecast_date > CURRENT_DATE()
      AND forecast_date <= DATE_ADD(CURRENT_DATE(), INTERVAL 90 DAY)
  )
  SELECT date, actual_revenue as revenue, data_type FROM historical
  UNION ALL
  SELECT date, forecasted_revenue as revenue, data_type FROM forecast_data
  ORDER BY date

Dimension (X-Axis): Date
Metrics (Y-Axis):
  - Actual Revenue (Line, blue, width 2px)
  - Forecasted Revenue (Line, orange dashed, width 2px)

Additional Features:
  - Trend line on historical data
  - Date range control (default: Last 12 months + 90 days forward)
  - Enable comparison feature (e.g., compare YoY)
  - Confidence interval shading for forecast (if using Prophet)

SECTION 1C: CATEGORY PERFORMANCE TABLE
────────────────────────────────────────────────────────────────────────────────

Chart Type: Table
Title: "Revenue by Product Category - Last 30 Days vs. 30-Day Forecast"
Height: 300px (spanning full width)

Data Query:
  SELECT 
    product_category,
    ROUND(SUM(CASE WHEN transaction_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) 
                   THEN total_revenue ELSE 0 END), 2) as revenue_last_30d,
    ROUND(AVG(CASE WHEN transaction_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) 
                   THEN daily_revenue ELSE 0 END), 2) as avg_daily_revenue,
    COUNT(DISTINCT transaction_id) as num_transactions,
    ROUND(AVG(unit_price), 2) as avg_unit_price,
    ROUND(SUM(quantity_sold), 0) as total_units_sold
  FROM transactions
  WHERE transaction_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  GROUP BY product_category
  ORDER BY revenue_last_30d DESC

Columns (Dimensions & Metrics):
  1. Product Category (Dimension)
  2. Revenue (Last 30D) - Currency format
  3. Avg Daily Revenue - Currency format
  4. # Transactions - Number format
  5. Avg Unit Price - Currency format
  6. Total Units Sold - Number format

Formatting:
  - Conditional formatting: Revenue column (green scale, highest=darkest)
  - Sortable by any column (default: Revenue descending)
  - Enable pagination (10 rows per page)

SECTION 1D: MONTH-OVER-MONTH GROWTH SPARKLINE
────────────────────────────────────────────────────────────────────────────────

Chart Type: Multiple sparklines (one per category)
Title: "MoM Revenue Trend by Category (Last 12 Months)"

Data Query (for each category):
  SELECT 
    DATE_TRUNC(transaction_date, MONTH) as month,
    SUM(total_revenue) as monthly_revenue
  FROM transactions
  WHERE product_category = '{category}'
    AND transaction_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)
  GROUP BY month
  ORDER BY month

Display: Inline sparklines in the category table above (as additional column)

================================================================================
TAB 2: INVENTORY RISK ALERTS & DEMAND-SUPPLY GAP ANALYSIS
================================================================================

Purpose:
  Identify categories with high demand forecast vs. current average stock
  levels to prevent stockouts and optimize inventory planning

Data Source Tables:
  - demand_forecast (90-day forecast)
  - transactions (historical patterns)
  - inventory_levels (assumed table with current stock)
  - average_stock_levels (aggregated inventory metrics)

SECTION 2A: RISK ALERT SCORECARD (4 Cards)
────────────────────────────────────────────────────────────────────────────────

1. Categories at Inventory Risk
   - Metric Query:
     SELECT COUNT(DISTINCT product_category) as categories_at_risk
     FROM (
       SELECT 
         product_category,
         AVG(daily_revenue) as avg_daily_demand,
         (SELECT AVG(stock_level) FROM inventory_levels) as avg_stock
       FROM daily_sales_aggregated
       WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
       GROUP BY product_category
       HAVING avg_daily_demand * 30 > avg_stock
     )
   
   - Format: Large number with warning icon
   - Color: Red if > 3, Yellow if 1-3, Green if 0

2. Total Forecasted Demand Gap
   - Metric Query:
     SELECT ROUND(SUM(demand_gap), 2) as total_demand_gap
     FROM (
       SELECT 
         df.forecasted_revenue - COALESCE(inv.available_stock, 0) as demand_gap
       FROM demand_forecast df
       LEFT JOIN inventory_levels inv ON df.product_category = inv.category
       WHERE df.forecast_date = CURRENT_DATE()
     )
   
   - Format: Currency ($)
   - Color: Red (warning color)

3. Highest Risk Category
   - Metric Query:
     SELECT TOP 1 product_category
     FROM risk_assessment
     ORDER BY risk_score DESC
   
   - Format: Text/Dimension
   - Icon: Alert icon

4. Days of Inventory Coverage
   - Metric Query:
     SELECT ROUND(
       AVG(current_stock_level) / NULLIF(AVG(daily_consumption), 0)
     , 1) as avg_days_of_inventory
     FROM inventory_analysis
   
   - Format: Number (days)
   - Target: > 30 days
   - Status: Green if > 30, Yellow if 20-30, Red if < 20

SECTION 2B: INVENTORY RISK HEAT MAP
────────────────────────────────────────────────────────────────────────────────

Chart Type: Table with conditional formatting
Title: "Inventory Risk Assessment by Category"
Height: 400px (spanning full width)

Data Query:
  SELECT 
    product_category,
    ROUND(SUM(quantity_sold), 0) as avg_daily_units,
    ROUND(AVG(daily_revenue), 2) as avg_daily_revenue,
    (SELECT AVG(stock_level) FROM inventory_levels) as current_stock,
    ROUND(
      (SELECT AVG(stock_level) FROM inventory_levels) / 
      NULLIF(ROUND(SUM(quantity_sold), 0), 0)
    , 1) as days_of_inventory,
    CASE 
      WHEN ((SELECT AVG(stock_level) FROM inventory_levels) / 
            NULLIF(ROUND(SUM(quantity_sold), 0), 0)) < 7 THEN 'CRITICAL'
      WHEN ((SELECT AVG(stock_level) FROM inventory_levels) / 
            NULLIF(ROUND(SUM(quantity_sold), 0), 0)) < 14 THEN 'HIGH'
      WHEN ((SELECT AVG(stock_level) FROM inventory_levels) / 
            NULLIF(ROUND(SUM(quantity_sold), 0), 0)) < 30 THEN 'MEDIUM'
      ELSE 'LOW'
    END as risk_level,
    ROUND(90_day_forecast.total / NULLIF(ROUND(SUM(quantity_sold), 0), 0), 1) as forecast_coverage
  FROM transactions
  LEFT JOIN 90_day_forecast ON transactions.product_category = 90_day_forecast.category
  WHERE transaction_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  GROUP BY product_category
  ORDER BY risk_level DESC, days_of_inventory ASC

Columns:
  1. Product Category - Text
  2. Avg Daily Units - Number
  3. Avg Daily Revenue - Currency
  4. Current Stock - Number
  5. Days of Inventory - Number (formatted as "X days")
  6. Risk Level - Text with background color:
     * CRITICAL (red)
     * HIGH (orange)
     * MEDIUM (yellow)
     * LOW (green)
  7. 90-Day Forecast Coverage - Number (formatted as "X days")

Conditional Formatting:
  - Background color gradient for "Days of Inventory" column
  - Text highlighting for "Risk Level" column

Sorting: Default by Risk Level (CRITICAL first)

SECTION 2C: DEMAND vs. INVENTORY FORECAST CHART
────────────────────────────────────────────────────────────────────────────────

Chart Type: Combo Chart (Area + Line)
Title: "90-Day Demand Forecast vs. Current Inventory Levels"
Height: 350px (spanning full width)

Data Query:
  SELECT 
    forecast_date as date,
    product_category,
    forecasted_units as demand,
    current_inventory as supply
  FROM demand_forecast df
  LEFT JOIN inventory_levels inv ON df.product_category = inv.category
  WHERE forecast_date <= DATE_ADD(CURRENT_DATE(), INTERVAL 90 DAY)
  ORDER BY date, product_category

Dimensions:
  - X-Axis: Date
  - Category: Product Category (color-coded, one area per category)

Metrics:
  - Forecasted Demand (area chart, semi-transparent, colored)
  - Current Inventory (line chart, dashed, darker)

Interactive Features:
  - Highlight categories above inventory threshold
  - Category filter (default: show all)

SECTION 2D: RISK TRENDS - TOP 5 CATEGORIES
────────────────────────────────────────────────────────────────────────────────

Chart Type: Column Chart (Stacked or Multi-Series)
Title: "Inventory Risk Trend - Top 5 At-Risk Categories"
Height: 300px (spanning 2/3 width)

Data Query:
  SELECT 
    DATE_TRUNC(date, WEEK) as week,
    product_category,
    ROUND(SUM(daily_demand), 0) as weekly_demand,
    ROUND(AVG(stock_level), 0) as avg_stock
  FROM risk_assessment
  WHERE product_category IN (
    SELECT TOP 5 product_category 
    FROM risk_assessment 
    WHERE date = CURRENT_DATE()
    ORDER BY risk_score DESC
  )
  AND date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
  GROUP BY week, product_category
  ORDER BY week, product_category

Axes:
  - X-Axis: Week
  - Y-Axis: Quantity (dual axis if needed for demand vs. stock)

Series:
  - Weekly Demand (stacked or separate)
  - Average Stock (stacked or separate)

================================================================================
TAB 3: CUSTOMER SEGMENTATION INSIGHTS & HIGH-VALUE USER TARGETING
================================================================================

Purpose:
  Visualize K-Means customer clusters, identify high-value segments,
  and provide actionable insights for targeted marketing campaigns

Data Source Tables:
  - customer_segments (BigQuery ML predictions with cluster assignments)
  - rfm_features (RFM metrics for each customer)
  - transactions (for segment behavioral patterns)

SECTION 3A: SEGMENTATION OVERVIEW (3 Cards)
────────────────────────────────────────────────────────────────────────────────

1. Total Unique Customers
   - Metric Query:
     SELECT COUNT(DISTINCT customer_id) as total_customers
     FROM customer_segments
   
   - Format: Large number with customer icon
   - Comparison: vs. last 30 days

2. Average CLV (Customer Lifetime Value) by Segment
   - Metric Query:
     SELECT ROUND(AVG(monetary_value), 2) as avg_clv
     FROM customer_segments
     WHERE assigned_cluster IS NOT NULL
   
   - Format: Currency ($)
   - Size: Medium card

3. High-Value Customer Concentration
   - Metric Query:
     SELECT ROUND(
       100 * SUM(CASE WHEN assigned_cluster = (
         SELECT assigned_cluster 
         FROM customer_segments 
         ORDER BY AVG(monetary_value) DESC LIMIT 1
       ) THEN 1 ELSE 0 END) / COUNT(*), 2
     ) as pct_revenue_from_top_cluster
     FROM customer_segments
   
   - Format: Percentage
   - Context: "% of revenue from top cluster"

SECTION 3B: CLUSTER SIZE & VALUE DISTRIBUTION
────────────────────────────────────────────────────────────────────────────────

Chart Type: Pie Chart or Donut Chart
Title: "Customer Distribution Across Clusters"
Height: 300px (spanning 1/2 width)

Data Query:
  SELECT 
    assigned_cluster,
    cluster_name,
    COUNT(DISTINCT customer_id) as num_customers,
    ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as pct_total_customers,
    ROUND(SUM(monetary_value), 2) as total_segment_revenue,
    ROUND(100 * SUM(monetary_value) / SUM(SUM(monetary_value)) OVER (), 2) as pct_total_revenue
  FROM customer_segments
  WHERE assigned_cluster IS NOT NULL
  GROUP BY assigned_cluster, cluster_name
  ORDER BY total_segment_revenue DESC

Dimension (Pie slices):
  - Cluster Name (label)
  - Count of customers (size of slice)

Tooltip:
  - Cluster Name
  - # Customers
  - % of Total Customers
  - Total Revenue
  - % of Total Revenue

Colors: Assign distinct colors to each cluster

SECTION 3C: AVERAGE METRICS BY CLUSTER TABLE
────────────────────────────────────────────────────────────────────────────────

Chart Type: Table
Title: "Cluster Profile - Key RFM Metrics"
Height: 350px (spanning 1/2 width)

Data Query:
  SELECT 
    assigned_cluster,
    cluster_name,
    COUNT(DISTINCT customer_id) as num_customers,
    ROUND(AVG(recency_days), 1) as avg_recency_days,
    ROUND(AVG(frequency_purchases), 1) as avg_frequency,
    ROUND(AVG(monetary_value), 2) as avg_ltv,
    ROUND(AVG(avg_transaction_value), 2) as avg_order_value,
    ROUND(AVG(distinct_categories_purchased), 1) as avg_categories,
    ROUND(SUM(total_quantity_purchased) / COUNT(*), 1) as avg_units_per_customer,
    CASE 
      WHEN AVG(monetary_value) > (SELECT PERCENTILE_CONT(monetary_value, 0.75) 
                                   FROM customer_segments)
           AND AVG(recency_days) < 60 THEN 'VIP_ACTIVE'
      WHEN AVG(monetary_value) > (SELECT PERCENTILE_CONT(monetary_value, 0.5) 
                                   FROM customer_segments) THEN 'HIGH_VALUE'
      WHEN AVG(recency_days) > 180 THEN 'AT_RISK'
      ELSE 'STANDARD'
    END as segment_label
  FROM customer_segments
  WHERE assigned_cluster IS NOT NULL
  GROUP BY assigned_cluster, cluster_name
  ORDER BY avg_ltv DESC

Columns:
  1. Cluster - Text
  2. # Customers - Number
  3. Avg Recency (days) - Number
  4. Avg Frequency - Number
  5. Avg LTV ($) - Currency (conditional formatting: gradient green)
  6. Avg Order Value ($) - Currency
  7. Avg Categories - Number
  8. Avg Units/Customer - Number
  9. Segment Label - Text (with color-coded background)

Sorting: Default by Avg LTV (descending)

SECTION 3D: TOP 10 HIGH-VALUE CUSTOMERS BY CLUSTER
────────────────────────────────────────────────────────────────────────────────

Chart Type: Table (filterable by cluster)
Title: "Top 10 High-Value Customers - Select Cluster to View"
Height: 350px (spanning full width)

Data Query:
  SELECT 
    assigned_cluster,
    cluster_name,
    customer_id,
    monetary_value,
    frequency_purchases,
    recency_days,
    avg_transaction_value,
    distinct_categories_purchased,
    segment_label,
    ROW_NUMBER() OVER (PARTITION BY assigned_cluster ORDER BY monetary_value DESC) AS rank_in_cluster
  FROM customer_segments
  WHERE assigned_cluster IS NOT NULL
  QUALIFY rank_in_cluster <= 10
  ORDER BY assigned_cluster, rank_in_cluster

Columns:
  1. Cluster - Dimension (filterable)
  2. Rank - Number
  3. Customer ID - Text (clickable link to CRM if available)
  4. LTV ($) - Currency (green highlight)
  5. # Purchases - Number
  6. Days Since Purchase - Number (with status: Green if < 30, Yellow 30-90, Red > 90)
  7. Avg Order Value ($) - Currency
  8. # Categories - Number
  9. Segment - Text

Interactivity:
  - Filter control: Select cluster from dropdown
  - Drill-down: Click customer ID to show transaction history (optional)

Conditional Formatting:
  - LTV column: Green gradient (highest = darkest green)
  - Recency column: Red if > 90, Yellow if 30-90, Green if < 30

SECTION 3E: CLUSTER HEATMAP - RFM SCORES
────────────────────────────────────────────────────────────────────────────────

Chart Type: Table (Heatmap style)
Title: "RFM Score Heatmap - Recency, Frequency, Monetary Ratings"
Height: 250px (spanning full width)

Data Query:
  SELECT 
    assigned_cluster,
    cluster_name,
    ROUND(AVG(recency_score), 1) as avg_recency_score,
    ROUND(AVG(frequency_score), 1) as avg_frequency_score,
    ROUND(AVG(monetary_score), 1) as avg_monetary_score,
    (ROUND(AVG(recency_score), 1) + ROUND(AVG(frequency_score), 1) + 
     ROUND(AVG(monetary_score), 1)) / 3 as overall_rfm_score
  FROM customer_segments
  WHERE assigned_cluster IS NOT NULL
  GROUP BY assigned_cluster, cluster_name
  ORDER BY overall_rfm_score DESC

Columns:
  1. Cluster - Text
  2. Recency Score (1-5) - Number with background color (red=low, green=high)
  3. Frequency Score (1-5) - Number with background color
  4. Monetary Score (1-5) - Number with background color
  5. Overall RFM Score - Number with prominent highlighting

Color Scheme for Scores:
  - 1-2: Red (poor)
  - 2-3: Orange (fair)
  - 3-4: Yellow (good)
  - 4-5: Green (excellent)

SECTION 3F: CLUSTER COMPARISON MATRIX (Optional Advanced)
────────────────────────────────────────────────────────────────────────────────

Chart Type: Bullet Chart or Comparison Chart
Title: "Cluster Performance Metrics Comparison"
Height: 300px (spanning full width)

Comparison Metrics:
  - Repeat Purchase Rate (%)
  - Average Days to Repurchase
  - Customer Retention Rate (%)
  - Average Basket Size ($)
  - Product Diversity (# of categories purchased)

Display: Bullet chart with cluster comparisons across metrics

================================================================================
GLOBAL DASHBOARD FEATURES
================================================================================

DATE CONTROLS:
  - Location: Top bar of each tab
  - Default: Last 12 months + 90 days forward
  - Presets:
    * Last 30 days
    * Last 90 days
    * Last 12 months
    * YTD (Year-to-Date)
    * Custom range
  - Applied to: Tabs 1 & 2 primarily

FILTERS:
  - Product Category filter (applies to Tabs 1 & 2)
  - Customer Segment filter (applies to Tab 3)
  - Region filter (if available in data)

REFRESH SETTINGS:
  - Automatic refresh: Every 4 hours
  - Manual refresh button: Top right corner
  - Last refresh timestamp: Bottom footer

COLOR PALETTE:
  - Primary (Blue): #1F77B4 - Revenue, positive metrics
  - Secondary (Orange): #FF7F0E - Forecasts, caution
  - Success (Green): #2CA02C - Targets met, healthy status
  - Warning (Red): #D62728 - Alerts, risk indicators
  - Neutral (Gray): #7F7F7F - Supporting information

FOOTER:
  - Data source: BigQuery dataset name & table references
  - Last refreshed timestamp
  - Forecast model versions (Prophet/ARIMA)
  - Dashboard version/updated date

================================================================================
BIGQUERY DATA MODEL FOR LOOKER STUDIO
================================================================================

Required Tables/Views for Looker Studio Connection:

1. transactions (Base fact table)
   Columns: transaction_id, transaction_date, product_category, customer_id,
            quantity_sold, unit_price, total_revenue, load_timestamp

2. daily_sales_aggregated (Pre-aggregated daily metrics - for performance)
   Columns: date, product_category, num_transactions, total_quantity,
            daily_revenue, avg_unit_price, avg_transaction_value

3. customer_segments (BigQuery ML predictions)
   Columns: customer_id, assigned_cluster, cluster_name, distance_to_cluster_center,
            recency_days, frequency_purchases, monetary_value, avg_transaction_value,
            distinct_categories_purchased, total_quantity_purchased,
            recency_score, frequency_score, monetary_score, segment_label,
            prediction_timestamp

4. rfm_features (Customer RFM aggregation)
   Columns: customer_id, recency_days, frequency_purchases, monetary_value,
            avg_transaction_value, distinct_categories_purchased,
            unique_purchase_days, calculation_timestamp

5. demand_forecast (90-day forecast output)
   Columns: forecast_date, product_category, forecasted_revenue,
            forecasted_units, confidence_interval_lower, confidence_interval_upper,
            model_type (prophet/arima), creation_timestamp

6. forecast_models_metrics (Model evaluation results)
   Columns: model_type, product_category, mae, mse, rmse, mape, accuracy,
            evaluation_date, model_version

================================================================================
IMPLEMENTATION CHECKLIST
================================================================================

☐ Step 1: Connect BigQuery dataset to Looker Studio
  - Create service account with BigQuery read permissions
  - Authorize Looker Studio to access BigQuery
  - Select tables: transactions, daily_sales_aggregated, customer_segments,
    rfm_features, demand_forecast, forecast_models_metrics

☐ Step 2: Create base report and set up data sources
  - Create new Looker Studio report
  - Add BigQuery data sources
  - Configure table relationships if needed

☐ Step 3: Build Tab 1 - Executive Revenue Trends
  - Add 4 KPI cards (Total Revenue YTD, Avg Daily, Forecast Accuracy, Gap)
  - Create combo chart (Historical vs. Forecast)
  - Add category performance table
  - Add MoM sparklines

☐ Step 4: Build Tab 2 - Inventory Risk Alerts
  - Add 4 risk alert cards
  - Create inventory risk heatmap table
  - Add demand vs. inventory forecast chart
  - Add risk trends chart for top 5 categories

☐ Step 5: Build Tab 3 - Customer Segmentation Insights
  - Add 3 segmentation overview cards
  - Create cluster distribution pie chart
  - Add cluster profile table
  - Add top 10 customers by cluster table
  - Add RFM heatmap
  - (Optional) Add comparison matrix

☐ Step 6: Add global controls and filters
  - Date range picker
  - Category dropdown filter
  - Segment filter
  - Refresh settings

☐ Step 7: Configure styling and branding
  - Apply color palette
  - Set fonts (Professional sans-serif)
  - Add company logo
  - Configure header and footer

☐ Step 8: Test and validate
  - Verify all charts load correctly
  - Test filters and date controls
  - Check performance (all queries < 10 seconds)
  - Validate data accuracy vs. BigQuery source

☐ Step 9: Set up sharing and access control
  - Share with stakeholders (Editor/Viewer roles)
  - Configure email notifications for alerts (if available)
  - Document dashboard usage guide

☐ Step 10: Configure BigQuery scheduled queries
  - Schedule daily_sales_aggregated refresh (10 PM daily)
  - Schedule forecast_models_metrics refresh (11 PM daily)
  - Set up alerts for failed jobs

================================================================================
PERFORMANCE OPTIMIZATION TIPS
================================================================================

1. Pre-aggregation Strategy:
   - Use daily_sales_aggregated table instead of querying transactions directly
   - This improves query performance by 10-100x

2. Partitioning:
   - Ensure all tables are partitioned by date
   - Use DATE_TRUNC in queries to prune partitions

3. Materialized Views:
   - Create BigQuery materialized views for complex aggregations
   - Automatically refresh daily

4. Query Caching:
   - Looker Studio caches results; leverage for identical filters

5. Denormalization:
   - Store pre-calculated metrics (RFM scores, segment labels) in tables
   - Avoid real-time calculations in dashboard

================================================================================
"""

# Export as module constant for use in Python/documentation
if __name__ == "__main__":
    print(LOOKER_STUDIO_DASHBOARD_BLUEPRINT)
    
    # Optionally save to file
    from config.config import OUTPUT_DIR
    output_file = OUTPUT_DIR / "Looker_Studio_Blueprint.txt"
    with open(output_file, 'w') as f:
        f.write(LOOKER_STUDIO_DASHBOARD_BLUEPRINT)
    print(f"\n✓ Blueprint saved to {output_file}")
