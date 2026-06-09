# Sales Demand Forecasting & Business Intelligence Dashboard

A Python-based data analytics project that generates synthetic retail transaction data, performs customer segmentation, creates demand forecasts, and produces dashboard-ready output files.

## Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Statsmodels ARIMA
- Prophet
- Matplotlib / Plotly
- Looker Studio Blueprint

## Project Features

- Generated 50,000+ synthetic retail transaction records
- Built an ETL pipeline for transaction processing
- Created customer segmentation using RFM analysis and K-Means clustering
- Implemented ARIMA-based demand forecasting across 12 product categories
- Generated dashboard-ready CSV files
- Created a Looker Studio dashboard blueprint for business intelligence reporting

## Project Structure

```text
sales-demand-forecasting-bi/
├── config/
│   ├── config.py
│   └── logging_config.py
├── src/
│   ├── phase1_etl/
│   │   ├── data_synthesis.py
│   │   └── etl_pipeline.py
│   ├── phase2_segmentation/
│   │   └── customer_segmentation.py
│   ├── phase3_forecasting/
│   │   └── demand_forecasting.py
│   └── phase4_dashboard/
│       └── dashboard_blueprint.py
├── output/
├── main.py
├── requirements.txt
├── README.md
└── PROJECT_SUMMARY.md