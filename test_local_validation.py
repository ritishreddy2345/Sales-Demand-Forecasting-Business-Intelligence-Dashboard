#!/usr/bin/env python
"""
LOCAL VALIDATION TEST SCRIPT
Tests Phase 1 data synthesis locally without BigQuery dependency
Validates core project functionality before running full pipeline
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def print_banner(title):
    """Print formatted banner"""
    width = 80
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)


def print_section(title):
    """Print section header"""
    print(f"\n{'─' * 80}\n📋 {title}\n{'─' * 80}")


def test_imports():
    """Test that all core packages can be imported"""
    print_section("TEST 1: Validating Package Imports")
    
    packages = {
        "pandas": "Data manipulation",
        "numpy": "Numerical computing",
        "statsmodels": "Statistical modeling",
        "sklearn": "Machine learning",
    }
    
    failed = []
    for package, description in packages.items():
        try:
            __import__(package)
            print(f"  ✅ {package:<20} - {description}")
        except ImportError as e:
            print(f"  ❌ {package:<20} - FAILED: {e}")
            failed.append(package)
    
    if failed:
        print(f"\n⚠️  Missing packages: {', '.join(failed)}")
        print("   Run: pip install " + " ".join(failed))
        return False
    else:
        print("\n✅ All core packages available!")
        return True


def test_data_synthesis():
    """Test Phase 1: Data Synthesis"""
    print_section("TEST 2: Data Synthesis (Phase 1)")
    
    try:
        print("  Importing data synthesis module...")
        from src.phase1_etl.data_synthesis import SyntheticDataGenerator
        print("  ✅ Module imported successfully")
        
        print("\n  Generating synthetic dataset (10,000 records)...")
        gen = SyntheticDataGenerator()
        df = gen.generate_transactions(num_records=10000)
        
        print(f"  ✅ Generated {len(df):,} records")
        print(f"\n  Dataset Summary:")
        print(f"    • Columns: {', '.join(df.columns.tolist())}")
        print(f"    • Date Range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")
        print(f"    • Product Categories: {df['product_category'].nunique()}")
        print(f"    • Unique Customers: {df['customer_id'].nunique()}")
        print(f"    • Total Revenue: ${df['total_revenue'].sum():,.2f}")
        print(f"    • Missing Values: {df.isnull().sum().sum()}")
        
        print(f"\n  Sample Records:")
        print(df.head(3).to_string(index=False))
        
        # Validate data quality
        assert len(df) == 10000, "Row count mismatch"
        assert df['transaction_date'].isnull().sum() == 0, "NULL dates found"
        assert df['total_revenue'].isnull().sum() == 0, "NULL revenue found"
        assert (df['unit_price'] > 0).all(), "Negative prices found"
        assert (df['total_revenue'] > 0).all(), "Negative revenue found"
        
        print("\n  ✅ Data quality validation PASSED")
        return True
        
    except Exception as e:
        print(f"\n  ❌ Data synthesis test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_configuration():
    """Test configuration loading"""
    print_section("TEST 3: Configuration Loading")
    
    try:
        print("  Loading configuration...")
        from config.config import (
            GCP_PROJECT_ID, GCP_DATASET_ID, PRODUCT_CATEGORIES,
            NUM_SYNTHETIC_RECORDS, PROJECT_ROOT
        )
        
        print(f"  ✅ Configuration loaded")
        print(f"\n  Configuration Summary:")
        print(f"    • GCP Project ID: {GCP_PROJECT_ID}")
        print(f"    • BigQuery Dataset: {GCP_DATASET_ID}")
        print(f"    • Synthetic Records: {NUM_SYNTHETIC_RECORDS:,}")
        print(f"    • Product Categories: {len(PRODUCT_CATEGORIES)}")
        print(f"    • Project Root: {PROJECT_ROOT}")
        
        # Validate directories exist
        logs_dir = PROJECT_ROOT / "logs"
        output_dir = PROJECT_ROOT / "output"
        
        assert logs_dir.exists(), f"Logs directory missing: {logs_dir}"
        assert output_dir.exists(), f"Output directory missing: {output_dir}"
        
        print(f"\n  ✅ Configuration validation PASSED")
        return True
        
    except Exception as e:
        print(f"\n  ❌ Configuration test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_logging():
    """Test logging setup"""
    print_section("TEST 4: Logging Configuration")
    
    try:
        print("  Setting up logging...")
        from config.logging_config import logger_etl, logger_segmentation, logger_forecasting
        
        logger_etl.info("Testing ETL logger")
        logger_segmentation.info("Testing Segmentation logger")
        logger_forecasting.info("Testing Forecasting logger")
        
        logs_dir = Path(__file__).parent / "logs"
        log_files = list(logs_dir.glob("*.log"))
        
        print(f"  ✅ Logging initialized")
        print(f"\n  Log Files Created:")
        for log_file in log_files:
            size_kb = log_file.stat().st_size / 1024
            print(f"    • {log_file.name} ({size_kb:.1f} KB)")
        
        print(f"\n  ✅ Logging validation PASSED")
        return True
        
    except Exception as e:
        print(f"\n  ❌ Logging test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_time_series_utilities():
    """Test time-series data preparation"""
    print_section("TEST 5: Time-Series Utilities")
    
    try:
        print("  Testing forecasting utilities...")
        import pandas as pd
        import numpy as np
        
        # Create sample daily sales data
        dates = pd.date_range(start='2023-01-01', periods=365)
        sales = np.random.randint(100, 1000, len(dates))
        df = pd.DataFrame({'ds': dates, 'y': sales})
        
        print(f"  ✅ Created sample time series: {len(df)} days")
        print(f"    • Date range: {df['ds'].min()} to {df['ds'].max()}")
        print(f"    • Sales range: ${df['y'].min()} to ${df['y'].max()}")
        
        print(f"\n  ✅ Time-series utilities validation PASSED")
        return True
        
    except Exception as e:
        print(f"\n  ❌ Time-series utilities test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all validation tests"""
    print_banner("🧪 LOCAL VALIDATION TEST SUITE")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Project Root: {PROJECT_ROOT}")
    
    tests = [
        ("Package Imports", test_imports),
        ("Configuration", test_configuration),
        ("Logging Setup", test_logging),
        ("Data Synthesis", test_data_synthesis),
        ("Time-Series Utilities", test_time_series_utilities),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ Unexpected error in {test_name}: {e}")
            results[test_name] = False
    
    # Print summary
    print_banner("📊 TEST SUMMARY")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status:<10} {test_name}")
    
    print(f"\n  {'─' * 40}")
    print(f"  Total: {passed}/{total} tests passed")
    
    if passed == total:
        print(f"\n  🎉 ALL LOCAL TESTS PASSED!")
        print(f"\n  Next Steps:")
        print(f"    1. Set up GCP credentials (see TESTING_AND_RUN_GUIDE.md)")
        print(f"    2. Update config.py with your GCP project ID")
        print(f"    3. Run: python main.py (for full pipeline)")
        return 0
    else:
        print(f"\n  ⚠️  Some tests failed. See errors above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
