"""
Configuration module for Sales Demand Forecasting & BI Dashboard
Centralized settings for BigQuery, paths, and project parameters
"""

import os
from pathlib import Path

# ============================================================================
# PROJECT PATHS
# ============================================================================
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
CONFIG_DIR = PROJECT_ROOT / "config"
LOGS_DIR = PROJECT_ROOT / "logs"
OUTPUT_DIR = PROJECT_ROOT / "output"
SQL_TEMPLATES_DIR = PROJECT_ROOT / "sql_templates"

# Create directories if they don't exist
for directory in [LOGS_DIR, OUTPUT_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================================================
# BIGQUERY CONFIGURATION
# ============================================================================
# Set these values based on your GCP project
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-project-id")
GCP_DATASET_ID = os.getenv("GCP_DATASET_ID", "sales_forecasting_db")
BIGQUERY_REGION = "US"  # Change if needed for your region

# Table names
TRANSACTIONS_TABLE = "transactions"
CUSTOMER_SEGMENTS_TABLE = "customer_segments"
RFM_FEATURES_TABLE = "rfm_features"
DAILY_SALES_TABLE = "daily_sales_aggregated"
FORECAST_TABLE = "demand_forecast"
MODELS_TABLE = "forecast_models_metrics"

# ============================================================================
# DATA SYNTHESIS PARAMETERS
# ============================================================================
NUM_SYNTHETIC_RECORDS = 50000
DATE_RANGE_DAYS = 1095  # 3 years
RANDOM_SEED = 42

PRODUCT_CATEGORIES = [
    "Electronics",
    "Apparel",
    "Home & Garden",
    "Sports & Outdoors",
    "Books",
    "Toys & Games",
    "Beauty & Personal Care",
    "Health & Wellness",
    "Kitchen & Dining",
    "Office Supplies",
    "Pet Supplies",
    "Automotive"
]

# ============================================================================
# TIME-SERIES FORECASTING PARAMETERS
# ============================================================================
FORECAST_HORIZON_DAYS = 90  # 90-day forecast
PROPHET_SEASONALITY_MODE = "additive"  # or "multiplicative"
PROPHET_YEARLY_SEASONALITY = True
PROPHET_WEEKLY_SEASONALITY = True
PROPHET_DAILY_SEASONALITY = False

# ARIMA parameters (will be auto-tuned, but these are defaults)
ARIMA_ORDER = (1, 1, 1)  # (p, d, q)
ARIMA_SEASONAL_ORDER = (1, 1, 1, 7)  # (P, D, Q, s) for weekly seasonality

# Forecast accuracy targets
TARGET_MAPE = 0.87  # 87% accuracy (13% error tolerance)

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============================================================================
# ETL PIPELINE SETTINGS
# ============================================================================
BATCH_SIZE = 10000  # Records per batch for BigQuery insert
LOAD_JOB_CONFIG_SKIP_LEADING_ROWS = 1
AUTO_DETECT_SCHEMA = True
TIME_PARTITIONING_FIELD = "transaction_date"

# ============================================================================
# CUSTOMER SEGMENTATION (K-MEANS)
# ============================================================================
KMEANS_NUM_CLUSTERS = 5  # Adjust based on business requirements
KMEANS_MAX_ITERATIONS = 20
KMEANS_INIT_METHOD = "random"  # or "kmeans++"

# RFM Thresholds (for manual segmentation if needed)
RFM_RECENCY_THRESHOLD_DAYS = 30
RFM_FREQUENCY_THRESHOLD = 5
RFM_MONETARY_THRESHOLD = 1000

# ============================================================================
# LOOKER STUDIO SETTINGS
# ============================================================================
LOOKER_DASHBOARD_UPDATE_INTERVAL = "daily"  # How often to refresh data
LOOKER_DEFAULT_DATE_RANGE = "last_12_months"

# KPI Targets
KPI_REVENUE_GROWTH_TARGET = 0.15  # 15% YoY growth
KPI_FORECAST_ACCURACY_TARGET = 0.87
KPI_CUSTOMER_RETENTION_TARGET = 0.85
KPI_AVG_ORDER_VALUE_TARGET = 100
