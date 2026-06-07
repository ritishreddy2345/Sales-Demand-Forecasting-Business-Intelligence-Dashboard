"""
Logging configuration for Sales Demand Forecasting project
Provides structured logging across all modules
"""

import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
from config.config import LOGS_DIR, LOG_LEVEL, LOG_FORMAT


def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    """
    Configure and return a logger instance
    
    Args:
        name: Logger name (typically __name__)
        log_file: Optional log file name (without path)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log_file specified)
    if log_file:
        log_path = LOGS_DIR / log_file
        file_handler = logging.handlers.RotatingFileHandler(
            log_path,
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(LOG_LEVEL)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Create loggers for different modules
logger_etl = setup_logger("ETL", "etl_pipeline.log")
logger_segmentation = setup_logger("Segmentation", "customer_segmentation.log")
logger_forecasting = setup_logger("Forecasting", "demand_forecasting.log")
logger_bigquery = setup_logger("BigQuery", "bigquery_operations.log")
