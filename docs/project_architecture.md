# Project Architecture

Synthetic Retail Data (50,000+ Transactions)
        |
        v
Python ETL Pipeline
        |
        v
Google BigQuery
        |
        +--> daily_sales_aggregated
        +--> monthly_sales_aggregated
        +--> category_sales_aggregated
        |
        +--> Customer Segmentation (BigQuery ML K-Means)
        |
        +--> Forecasting (Prophet + ARIMA)
        |
        v
Looker Studio Dashboard