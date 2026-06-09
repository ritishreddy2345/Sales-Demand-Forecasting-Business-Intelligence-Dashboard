import logging
from config.config import LOGS_DIR, LOG_FORMAT, LOG_LEVEL

def setup_logger(name: str, filename: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))

    if logger.handlers:
        return logger

    formatter = logging.Formatter(LOG_FORMAT)

    file_handler = logging.FileHandler(LOGS_DIR / filename, encoding="utf-8")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger

logger_etl = setup_logger("etl", "etl_pipeline.log")
logger_segmentation = setup_logger("segmentation", "customer_segmentation.log")
logger_forecasting = setup_logger("forecasting", "forecasting.log")
logger_bigquery = setup_logger("bigquery", "bigquery_operations.log")