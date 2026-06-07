"""
Sales Demand Forecasting & BI Dashboard Project
Main package initialization
"""

__version__ = "1.0.0"
__author__ = "Data Engineering Team"
__description__ = "End-to-end sales forecasting and business intelligence platform"

from config.logging_config import logger_etl, logger_segmentation, logger_forecasting, logger_bigquery

__all__ = [
    'logger_etl',
    'logger_segmentation', 
    'logger_forecasting',
    'logger_bigquery'
]
