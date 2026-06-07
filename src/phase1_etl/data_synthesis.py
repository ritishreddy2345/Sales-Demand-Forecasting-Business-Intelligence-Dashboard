"""
PHASE 1: Data Synthesis & Automated ETL Pipeline
Generates synthetic retail transaction data with realistic patterns
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple
from config.config import (
    NUM_SYNTHETIC_RECORDS,
    DATE_RANGE_DAYS,
    PRODUCT_CATEGORIES,
    RANDOM_SEED
)
from config.logging_config import logger_etl


class SyntheticDataGenerator:
    """Generates realistic synthetic retail transaction data"""
    
    def __init__(self, random_seed: int = RANDOM_SEED):
        """Initialize with random seed for reproducibility"""
        np.random.seed(random_seed)
        self.random_seed = random_seed
        logger_etl.info(f"SyntheticDataGenerator initialized with seed: {random_seed}")
    
    def _generate_dates(self, num_records: int) -> np.ndarray:
        """
        Generate dates spanning past 3 years with realistic distribution
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=DATE_RANGE_DAYS)
        
        # Generate dates with slight bias towards recent dates
        dates = np.random.choice(
            pd.date_range(start_date, end_date, freq='D'),
            size=num_records,
            p=None  # Uniform distribution
        )
        
        return pd.to_datetime(dates).date
    
    def _generate_seasonal_quantity(self, date: datetime, base: int = 5) -> int:
        """
        Generate quantity with seasonal trends
        - Higher during holiday seasons (Nov, Dec)
        - Lower during summer months
        """
        month = date.month
        day_of_year = date.timetuple().tm_yday
        
        # Holiday boost
        if month in [11, 12]:
            seasonal_factor = 1.4
        # Summer decline
        elif month in [6, 7, 8]:
            seasonal_factor = 0.8
        else:
            seasonal_factor = 1.0
        
        # Add weekly seasonality
        weekday_factor = 1.1 if date.weekday() < 5 else 0.95  # Higher on weekdays
        
        quantity = int(base * seasonal_factor * weekday_factor)
        return max(1, quantity)
    
    def _generate_unit_prices(self) -> dict:
        """Generate realistic unit prices by category"""
        price_ranges = {
            "Electronics": (100, 1500),
            "Apparel": (20, 150),
            "Home & Garden": (30, 500),
            "Sports & Outdoors": (25, 300),
            "Books": (10, 50),
            "Toys & Games": (15, 100),
            "Beauty & Personal Care": (10, 80),
            "Health & Wellness": (15, 200),
            "Kitchen & Dining": (20, 200),
            "Office Supplies": (5, 100),
            "Pet Supplies": (10, 150),
            "Automotive": (50, 500)
        }
        return price_ranges
    
    def generate_transactions(self, num_records: int = NUM_SYNTHETIC_RECORDS) -> pd.DataFrame:
        """
        Generate synthetic transaction data
        
        Returns:
            DataFrame with transaction records
        """
        logger_etl.info(f"Generating {num_records:,} synthetic transaction records...")
        
        # Generate base data
        dates = self._generate_dates(num_records)
        transaction_ids = np.arange(1000001, 1000001 + num_records)
        customer_ids = np.random.randint(1, 5001, num_records)  # 5000 unique customers
        categories = np.random.choice(PRODUCT_CATEGORIES, num_records)
        
        # Generate quantities with seasonality
        quantities = np.array([
            self._generate_seasonal_quantity(pd.Timestamp(date))
            for date in dates
        ])
        
        # Generate prices by category
        price_ranges = self._generate_unit_prices()
        unit_prices = np.array([
            np.random.uniform(*price_ranges[cat])
            for cat in categories
        ])
        
        # Calculate revenue
        total_revenue = quantities * unit_prices
        
        # Create DataFrame
        df = pd.DataFrame({
            'transaction_id': transaction_ids,
            'transaction_date': pd.to_datetime(dates),
            'product_category': categories,
            'customer_id': customer_ids,
            'quantity_sold': quantities,
            'unit_price': np.round(unit_prices, 2),
            'total_revenue': np.round(total_revenue, 2),
            'load_timestamp': datetime.now()
        })
        
        # Sort by date
        df = df.sort_values('transaction_date').reset_index(drop=True)
        
        logger_etl.info(
            f"Successfully generated {len(df):,} records\n"
            f"  - Date range: {df['transaction_date'].min().date()} to {df['transaction_date'].max().date()}\n"
            f"  - Unique customers: {df['customer_id'].nunique():,}\n"
            f"  - Total revenue: ${df['total_revenue'].sum():,.2f}\n"
            f"  - Average order value: ${df['total_revenue'].mean():.2f}"
        )
        
        return df
    
    def validate_data_quality(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Validate synthetic data quality
        
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        issues = []
        
        # Check for nulls
        if df.isnull().any().any():
            issues.append(f"Found {df.isnull().sum().sum()} null values")
        
        # Check for negatives
        if (df['quantity_sold'] < 0).any() or (df['unit_price'] < 0).any():
            issues.append("Found negative quantities or prices")
        
        # Check for zero transactions
        if (df['total_revenue'] == 0).any():
            issues.append("Found zero revenue transactions")
        
        # Check date range
        if df['transaction_date'].min().year < 2023:
            issues.append("Date range extends before 2023")
        
        # Check categories
        invalid_categories = set(df['product_category']) - set(PRODUCT_CATEGORIES)
        if invalid_categories:
            issues.append(f"Invalid categories found: {invalid_categories}")
        
        if issues:
            msg = "Data quality issues found:\n" + "\n".join([f"  - {i}" for i in issues])
            logger_etl.warning(msg)
            return False, msg
        else:
            msg = "Data quality validation passed ✓"
            logger_etl.info(msg)
            return True, msg
    
    def export_sample(self, df: pd.DataFrame, output_path: str, num_rows: int = 100):
        """Export sample data to CSV for inspection"""
        df.head(num_rows).to_csv(output_path, index=False)
        logger_etl.info(f"Sample data ({num_rows} rows) exported to {output_path}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    # Initialize generator
    generator = SyntheticDataGenerator()
    
    # Generate transactions
    transactions_df = generator.generate_transactions()
    
    # Validate data
    is_valid, validation_msg = generator.validate_data_quality(transactions_df)
    
    # Export sample
    from config.config import OUTPUT_DIR
    generator.export_sample(transactions_df, OUTPUT_DIR / "sample_transactions.csv")
    
    print("\n" + "="*80)
    print("PHASE 1: DATA SYNTHESIS COMPLETE")
    print("="*80)
    print(f"Records generated: {len(transactions_df):,}")
    print(f"Data quality: {'✓ PASSED' if is_valid else '✗ FAILED'}")
    print(f"Sample exported to: output/sample_transactions.csv")
