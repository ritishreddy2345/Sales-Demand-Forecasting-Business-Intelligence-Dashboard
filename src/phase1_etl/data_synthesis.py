import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple

from config.config import (
    NUM_SYNTHETIC_RECORDS,
    DATE_RANGE_DAYS,
    PRODUCT_CATEGORIES,
    RANDOM_SEED,
    TRANSACTIONS_CSV,
)
from config.logging_config import logger_etl


class SyntheticDataGenerator:
    def __init__(self, random_seed: int = RANDOM_SEED):
        np.random.seed(random_seed)
        self.random_seed = random_seed

    def _generate_dates(self, num_records: int):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=DATE_RANGE_DAYS)
        return np.random.choice(
            pd.date_range(start_date, end_date, freq="D"),
            size=num_records
        )

    def _generate_seasonal_quantity(self, date) -> int:
        month = date.month

        if month in [11, 12]:
            seasonal_factor = 1.4
        elif month in [6, 7, 8]:
            seasonal_factor = 0.85
        else:
            seasonal_factor = 1.0

        weekday_factor = 1.1 if date.weekday() < 5 else 0.95
        base_quantity = np.random.randint(1, 8)

        quantity = int(base_quantity * seasonal_factor * weekday_factor)
        return max(1, quantity)

    def _price_ranges(self):
        return {
            "Electronics": (100, 1500),
            "Clothing": (20, 150),
            "Home & Kitchen": (30, 500),
            "Beauty": (10, 80),
            "Sports": (25, 300),
            "Books": (10, 50),
            "Automotive": (50, 500),
            "Toys": (15, 100),
            "Groceries": (5, 100),
            "Health": (15, 200),
            "Garden": (30, 400),
            "Office Supplies": (5, 100),
        }

    def generate_transactions(self, num_records: int = NUM_SYNTHETIC_RECORDS) -> pd.DataFrame:
        logger_etl.info(f"Generating {num_records:,} synthetic records")

        dates = self._generate_dates(num_records)
        categories = np.random.choice(PRODUCT_CATEGORIES, num_records)
        price_ranges = self._price_ranges()

        quantities = np.array([
            self._generate_seasonal_quantity(pd.Timestamp(date))
            for date in dates
        ])

        unit_prices = np.array([
            np.random.uniform(*price_ranges[category])
            for category in categories
        ])

        df = pd.DataFrame({
            "transaction_id": np.arange(1000001, 1000001 + num_records),
            "transaction_date": pd.to_datetime(dates),
            "product_category": categories,
            "customer_id": np.random.randint(1, 5001, num_records),
            "quantity_sold": quantities,
            "unit_price": np.round(unit_prices, 2),
        })

        df["total_revenue"] = np.round(df["quantity_sold"] * df["unit_price"], 2)
        df["load_timestamp"] = datetime.now()
        df = df.sort_values("transaction_date").reset_index(drop=True)

        return df

    def validate_data_quality(self, df: pd.DataFrame) -> Tuple[bool, str]:
        issues = []

        if df.empty:
            issues.append("DataFrame is empty")

        if df.isnull().sum().sum() > 0:
            issues.append("Null values found")

        if (df["quantity_sold"] <= 0).any():
            issues.append("Invalid quantity found")

        if (df["unit_price"] <= 0).any():
            issues.append("Invalid price found")

        if (df["total_revenue"] <= 0).any():
            issues.append("Invalid revenue found")

        if issues:
            return False, "; ".join(issues)

        return True, "Data quality validation passed"

    def export_transactions(self, df: pd.DataFrame):
        df.to_csv(TRANSACTIONS_CSV, index=False)
        logger_etl.info(f"Transactions saved to {TRANSACTIONS_CSV}")


if __name__ == "__main__":
    generator = SyntheticDataGenerator()
    df = generator.generate_transactions()
    is_valid, message = generator.validate_data_quality(df)

    print(message)

    if is_valid:
        generator.export_transactions(df)
        print(f"Generated file: {TRANSACTIONS_CSV}")