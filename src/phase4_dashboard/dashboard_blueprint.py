from config.config import (
    OUTPUT_DIR,
    TRANSACTIONS_CSV,
    DAILY_SALES_CSV,
    CUSTOMER_SEGMENTS_CSV,
    FORECAST_RESULTS_CSV,
    MODEL_METRICS_CSV,
)
from config.logging_config import logger_etl


LOOKER_STUDIO_DASHBOARD_BLUEPRINT = f"""
# Sales Demand Forecasting & Business Intelligence Dashboard

## Project Overview

This dashboard uses locally generated CSV outputs from the project pipeline.

## Output Files Used

1. Transactions Data:
   {TRANSACTIONS_CSV}

2. Daily Sales Aggregated Data:
   {DAILY_SALES_CSV}

3. Customer Segments:
   {CUSTOMER_SEGMENTS_CSV}

4. Forecast Results:
   {FORECAST_RESULTS_CSV}

5. Forecast Model Metrics:
   {MODEL_METRICS_CSV}

---

## Dashboard Tab 1: Revenue Trends & Forecasting

### KPIs
- Total Revenue
- Average Daily Revenue
- Total Transactions
- Forecast Accuracy

### Charts
- Historical daily revenue trend
- 90-day forecasted revenue by category
- Category-wise revenue performance
- Prophet vs ARIMA model comparison

### Recommended Data Source
Use:
- transactions.csv
- daily_sales_aggregated.csv
- forecast_results.csv
- forecast_model_metrics.csv

---

## Dashboard Tab 2: Inventory Risk Alerts

### Purpose
Identify categories where forecasted demand is high and may require inventory planning.

### Suggested KPIs
- Highest forecasted category
- Average forecasted revenue
- Top 5 high-demand categories
- Category risk level

### Suggested Logic
Risk can be calculated using forecasted revenue:

- HIGH: Forecasted revenue above 75th percentile
- MEDIUM: Forecasted revenue between 40th and 75th percentile
- LOW: Forecasted revenue below 40th percentile

### Recommended Data Source
Use:
- forecast_results.csv
- daily_sales_aggregated.csv

---

## Dashboard Tab 3: Customer Segmentation Insights

### KPIs
- Total Customers
- VIP Active Customers
- High Value Customers
- At Risk Customers

### Charts
- Customer count by segment label
- Cluster-wise monetary value
- Average frequency by segment
- Recency vs monetary value scatter plot

### Recommended Data Source
Use:
- customer_segments.csv

---

## Recommended Looker Studio Steps

1. Open Looker Studio.
2. Create a blank report.
3. Add CSV files as data sources.
4. Start with customer_segments.csv and forecast_results.csv.
5. Create three pages:
   - Revenue Forecasting
   - Inventory Risk
   - Customer Segmentation
6. Add filters:
   - Product Category
   - Model
   - Customer Segment
7. Add date range control for transaction_date and forecast_date.

---

## GitHub Project Outputs

After successful execution, include these files in the repository:

- output/transactions.csv
- output/daily_sales_aggregated.csv
- output/customer_segments.csv
- output/forecast_results.csv
- output/forecast_model_metrics.csv
- output/Looker_Studio_Complete_Blueprint.md

---

## Resume-Friendly Project Description

Sales Demand Forecasting & Business Intelligence Dashboard

- Built an end-to-end Python ETL pipeline generating and processing 50,000+ retail transaction records.
- Created customer segmentation using RFM analysis and K-Means clustering.
- Developed demand forecasting models using Prophet and ARIMA across 12 product categories.
- Generated dashboard-ready CSV outputs for revenue trends, inventory risk analysis, and customer insights.
- Designed a Looker Studio dashboard blueprint for KPI tracking and data-driven business planning.
"""


class DashboardBlueprint:
    def generate_blueprint(self) -> bool:
        try:
            output_file = OUTPUT_DIR / "Looker_Studio_Complete_Blueprint.md"

            with open(output_file, "w", encoding="utf-8") as file:
                file.write(LOOKER_STUDIO_DASHBOARD_BLUEPRINT)

            logger_etl.info(f"Dashboard blueprint saved to {output_file}")
            print(f"Phase 4 completed successfully. File created: {output_file}")
            return True

        except Exception as e:
            logger_etl.error(f"Phase 4 failed: {str(e)}")
            print(f"Phase 4 failed: {str(e)}")
            return False


if __name__ == "__main__":
    dashboard = DashboardBlueprint()
    dashboard.generate_blueprint()