"""
PHASE 1: Automated ETL Pipeline to BigQuery
Handles dataset/table creation, branching logic, and robust error handling
"""

import pandas as pd
from typing import Tuple
from datetime import datetime
from config.logging_config import logger_etl
from config.config import (
    GCP_PROJECT_ID,
    GCP_DATASET_ID,
    TRANSACTIONS_TABLE,
    BATCH_SIZE
)
from src.bigquery_utils import BigQueryManager
from src.phase1_etl.data_synthesis import SyntheticDataGenerator


class ETLPipeline:
    """Main ETL pipeline orchestrator"""
    
    def __init__(self, project_id: str = GCP_PROJECT_ID):
        """Initialize ETL pipeline"""
        self.bq_manager = BigQueryManager(project_id)
        self.generator = SyntheticDataGenerator()
        logger_etl.info("ETL Pipeline initialized")
    
    def check_infrastructure(self) -> Tuple[bool, dict]:
        """
        Check and create BigQuery infrastructure (dataset, tables)
        Implements branching logic:
        - If dataset exists: check for tables
        - If dataset doesn't exist: create dataset and initialize schema
        
        Returns:
            Tuple of (success: bool, status_dict: dict)
        """
        status = {
            'dataset_created': False,
            'dataset_exists': False,
            'table_exists': False,
            'table_created': False,
            'messages': []
        }
        
        try:
            logger_etl.info("=" * 80)
            logger_etl.info("CHECKING BIGQUERY INFRASTRUCTURE")
            logger_etl.info("=" * 80)
            
            # BRANCH 1: Check if dataset exists
            if self.bq_manager.dataset_exists():
                status['dataset_exists'] = True
                msg = f"✓ Dataset '{GCP_DATASET_ID}' already exists"
                logger_etl.info(msg)
                status['messages'].append(msg)
                
                # BRANCH 1A: Check if table exists
                if self.bq_manager.table_exists(TRANSACTIONS_TABLE):
                    status['table_exists'] = True
                    msg = f"✓ Table '{TRANSACTIONS_TABLE}' already exists - will APPEND data"
                    logger_etl.info(msg)
                    status['messages'].append(msg)
                else:
                    msg = f"✗ Table '{TRANSACTIONS_TABLE}' does not exist - will CREATE"
                    logger_etl.info(msg)
                    status['messages'].append(msg)
            
            # BRANCH 2: Dataset doesn't exist - create it
            else:
                msg = f"✗ Dataset '{GCP_DATASET_ID}' not found - CREATING..."
                logger_etl.info(msg)
                status['messages'].append(msg)
                
                if self.bq_manager.create_dataset():
                    status['dataset_created'] = True
                    msg = f"✓ Dataset '{GCP_DATASET_ID}' created successfully"
                    logger_etl.info(msg)
                    status['messages'].append(msg)
                else:
                    msg = f"✗ Failed to create dataset '{GCP_DATASET_ID}'"
                    logger_etl.error(msg)
                    status['messages'].append(msg)
                    return False, status
            
            return True, status
        
        except Exception as e:
            error_msg = f"Error checking infrastructure: {str(e)}"
            logger_etl.error(error_msg)
            status['messages'].append(error_msg)
            return False, status
    
    def load_data_to_bigquery(
        self,
        df: pd.DataFrame,
        write_disposition: str = "WRITE_APPEND"
    ) -> Tuple[bool, str]:
        """
        Load DataFrame to BigQuery with batching
        
        Args:
            df: DataFrame to load
            write_disposition: "WRITE_APPEND", "WRITE_TRUNCATE", or "WRITE_IF_EMPTY"
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            logger_etl.info("=" * 80)
            logger_etl.info("LOADING DATA TO BIGQUERY")
            logger_etl.info("=" * 80)
            
            total_records = len(df)
            num_batches = (total_records // BATCH_SIZE) + (1 if total_records % BATCH_SIZE else 0)
            
            logger_etl.info(f"Total records: {total_records:,}")
            logger_etl.info(f"Batch size: {BATCH_SIZE:,}")
            logger_etl.info(f"Number of batches: {num_batches}")
            
            # Load data (BigQuery SDK handles batching internally)
            success, message = self.bq_manager.insert_dataframe(
                df,
                TRANSACTIONS_TABLE,
                write_disposition=write_disposition,
                autodetect=True
            )
            
            if success:
                logger_etl.info("=" * 80)
                logger_etl.info(f"✓ DATA LOAD SUCCESSFUL")
                logger_etl.info("=" * 80)
            else:
                logger_etl.error(f"✗ DATA LOAD FAILED: {message}")
            
            return success, message
        
        except Exception as e:
            error_msg = f"Error loading data: {str(e)}"
            logger_etl.error(error_msg)
            return False, error_msg
    
    def run_etl_pipeline(self, generate_new_data: bool = True) -> bool:
        """
        Execute complete ETL pipeline
        
        Args:
            generate_new_data: If True, generate synthetic data; if False, use existing
        
        Returns:
            True if successful
        """
        try:
            logger_etl.info("\n" + "🚀 " * 20)
            logger_etl.info("STARTING ETL PIPELINE EXECUTION")
            logger_etl.info("🚀 " * 20 + "\n")
            
            # Step 1: Check infrastructure
            infra_ok, infra_status = self.check_infrastructure()
            if not infra_ok:
                logger_etl.error("Infrastructure check failed. Aborting pipeline.")
                return False
            
            # Step 2: Generate or retrieve data
            if generate_new_data:
                logger_etl.info("\n" + "=" * 80)
                logger_etl.info("STEP 1: GENERATING SYNTHETIC DATA")
                logger_etl.info("=" * 80)
                df = self.generator.generate_transactions()
                
                # Validate data
                is_valid, validation_msg = self.generator.validate_data_quality(df)
                if not is_valid:
                    logger_etl.error(f"Data validation failed: {validation_msg}")
                    return False
            
            # Step 3: Determine write disposition based on table existence
            if infra_status.get('table_exists'):
                write_disposition = "WRITE_APPEND"
                logger_etl.info(f"Table exists - using WRITE_APPEND disposition")
            else:
                write_disposition = "WRITE_TRUNCATE"
                logger_etl.info(f"Table does not exist - using WRITE_TRUNCATE disposition")
            
            # Step 4: Load data to BigQuery
            logger_etl.info("\n" + "=" * 80)
            logger_etl.info("STEP 2: LOADING DATA TO BIGQUERY")
            logger_etl.info("=" * 80)
            success, load_message = self.load_data_to_bigquery(df, write_disposition)
            
            if not success:
                logger_etl.error(f"Data load failed: {load_message}")
                return False
            
            # Final summary
            logger_etl.info("\n" + "✓ " * 20)
            logger_etl.info("ETL PIPELINE COMPLETED SUCCESSFULLY")
            logger_etl.info("✓ " * 20)
            
            return True
        
        except Exception as e:
            logger_etl.error(f"Fatal error in ETL pipeline: {str(e)}")
            return False


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    import sys
    import time
    
    # Initialize pipeline
    pipeline = ETLPipeline()
    
    # Run pipeline
    start_time = time.time()
    success = pipeline.run_etl_pipeline(generate_new_data=True)
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 80)
    print("PHASE 1 ETL PIPELINE EXECUTION SUMMARY")
    print("=" * 80)
    print(f"Status: {'✓ SUCCESS' if success else '✗ FAILED'}")
    print(f"Execution time: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
    print("=" * 80)
    
    sys.exit(0 if success else 1)
