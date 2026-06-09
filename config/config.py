import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
OUTPUT_DIR = BASE_DIR / "output"

for directory in [DATA_DIR, LOGS_DIR, OUTPUT_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# GCP Configuration
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "sales-demand-forecasting-bi")
GCP_DATASET_ID = os.getenv("GCP_DATASET_ID", "sales_forecasting_db")
BIGQUERY_REGION = os.getenv("BIGQUERY_REGION", "US")

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Data
NUM_SYNTHETIC_RECORDS = 50000
DATE_RANGE_DAYS = 1095
RANDOM_SEED = 42
BATCH_SIZE = 10000

PRODUCT_CATEGORIES = [
    "Electronics",
    "Clothing",
    "Home & Kitchen",
    "Beauty",
    "Sports",
    "Books",
    "Automotive",
    "Toys",
    "Groceries",
    "Health",
    "Garden",
    "Office Supplies",
]

# Simple table names only
TRANSACTIONS_TABLE = "transactions"
RFM_FEATURES_TABLE = "rfm_features"
CUSTOMER_SEGMENTS_TABLE = "customer_segments"
DAILY_SALES_TABLE = "daily_sales_aggregated"
DEMAND_FORECAST_TABLE = "demand_forecast"
MODEL_METRICS_TABLE = "forecast_models_metrics"

# Phase 2
KMEANS_NUM_CLUSTERS = 5
KMEANS_MAX_ITERATIONS = 20
KMEANS_INIT_METHOD = "k-means++"

# Phase 3
FORECAST_HORIZON_DAYS = 90
TARGET_ACCURACY = 0.87

PROPHET_SEASONALITY_MODE = "additive"
PROPHET_YEARLY_SEASONALITY = True
PROPHET_WEEKLY_SEASONALITY = True

ARIMA_ORDER = (1, 1, 1)
ARIMA_SEASONAL_ORDER = (1, 1, 1, 7)

# File paths
TRANSACTIONS_CSV = OUTPUT_DIR / "transactions.csv"
DAILY_SALES_CSV = OUTPUT_DIR / "daily_sales_aggregated.csv"
CUSTOMER_SEGMENTS_CSV = OUTPUT_DIR / "customer_segments.csv"
FORECAST_RESULTS_CSV = OUTPUT_DIR / "forecast_results.csv"
MODEL_METRICS_CSV = OUTPUT_DIR / "forecast_model_metrics.csv"