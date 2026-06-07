"""
BigQuery utilities for Sales Demand Forecasting project
Handles dataset/table creation, data insertion, and query execution
"""

from google.cloud import bigquery
from google.api_core.exceptions import NotFound, Conflict
import pandas as pd
from typing import Optional, List, Tuple
from config.logging_config import logger_bigquery
from config.config import (
    GCP_PROJECT_ID,
    GCP_DATASET_ID,
    BIGQUERY_REGION,
    BATCH_SIZE
)


class BigQueryManager:
    """Manages BigQuery operations with error handling and logging"""
    
    def __init__(self, project_id: str = GCP_PROJECT_ID):
        """
        Initialize BigQuery client
        
        Args:
            project_id: GCP project ID
        """
        self.project_id = project_id
        self.dataset_id = GCP_DATASET_ID
        self.client = bigquery.Client(project=project_id)
        logger_bigquery.info(f"BigQuery client initialized for project: {project_id}")
    
    def dataset_exists(self) -> bool:
        """Check if dataset exists"""
        try:
            self.client.get_dataset(self.dataset_id)
            logger_bigquery.info(f"Dataset '{self.dataset_id}' exists")
            return True
        except NotFound:
            logger_bigquery.warning(f"Dataset '{self.dataset_id}' not found")
            return False
    
    def create_dataset(self) -> bool:
        """
        Create dataset if it doesn't exist
        
        Returns:
            True if created or already exists
        """
        try:
            if not self.dataset_exists():
                dataset = bigquery.Dataset(f"{self.project_id}.{self.dataset_id}")
                dataset.location = BIGQUERY_REGION
                dataset = self.client.create_dataset(dataset)
                logger_bigquery.info(f"Dataset '{self.dataset_id}' created successfully")
            return True
        except Conflict:
            logger_bigquery.info(f"Dataset '{self.dataset_id}' already exists")
            return True
        except Exception as e:
            logger_bigquery.error(f"Error creating dataset: {str(e)}")
            raise
    
    def table_exists(self, table_id: str) -> bool:
        """Check if table exists"""
        try:
            self.client.get_table(f"{self.project_id}.{self.dataset_id}.{table_id}")
            return True
        except NotFound:
            return False
    
    def insert_dataframe(
        self,
        df: pd.DataFrame,
        table_id: str,
        write_disposition: str = "WRITE_APPEND",
        autodetect: bool = True
    ) -> Tuple[bool, str]:
        """
        Insert DataFrame into BigQuery table
        
        Args:
            df: Pandas DataFrame to insert
            table_id: Target table name
            write_disposition: "WRITE_APPEND", "WRITE_TRUNCATE", or "WRITE_IF_EMPTY"
            autodetect: Auto-detect schema from data
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            table_path = f"{self.project_id}.{self.dataset_id}.{table_id}"
            
            job_config = bigquery.LoadJobConfig(
                write_disposition=write_disposition,
                autodetect=autodetect,
                time_partitioning=bigquery.TimePartitioning(
                    type_=bigquery.TimePartitioningType.DAY,
                    field="transaction_date"
                ) if "transaction_date" in df.columns else None
            )
            
            load_job = self.client.load_table_from_dataframe(
                df,
                table_path,
                job_config=job_config
            )
            
            load_job.result()  # Wait for job to complete
            logger_bigquery.info(
                f"Loaded {len(df)} records into {table_id}. "
                f"Job ID: {load_job.job_id}"
            )
            return True, f"Successfully loaded {len(df)} records into {table_id}"
        
        except Exception as e:
            error_msg = f"Error inserting data into {table_id}: {str(e)}"
            logger_bigquery.error(error_msg)
            return False, error_msg
    
    def execute_query(self, query: str, timeout_seconds: int = 300) -> Optional[pd.DataFrame]:
        """
        Execute SQL query and return results as DataFrame
        
        Args:
            query: SQL query string
            timeout_seconds: Query timeout
        
        Returns:
            DataFrame with results or None if error
        """
        try:
            job_config = bigquery.QueryJobConfig()
            query_job = self.client.query(query, job_config=job_config, timeout=timeout_seconds)
            results_df = query_job.to_dataframe()
            logger_bigquery.info(f"Query executed successfully. Returned {len(results_df)} rows")
            return results_df
        except Exception as e:
            logger_bigquery.error(f"Error executing query: {str(e)}")
            return None
    
    def create_table_from_query(self, query: str, table_id: str) -> bool:
        """
        Create table from query results
        
        Args:
            query: SQL query
            table_id: Target table name
        
        Returns:
            True if successful
        """
        try:
            job_config = bigquery.QueryJobConfig(
                destination=f"{self.project_id}.{self.dataset_id}.{table_id}",
                write_disposition="WRITE_TRUNCATE"
            )
            
            query_job = self.client.query(query, job_config=job_config)
            query_job.result()
            logger_bigquery.info(f"Table '{table_id}' created from query")
            return True
        except Exception as e:
            logger_bigquery.error(f"Error creating table from query: {str(e)}")
            return False
    
    def get_table_schema(self, table_id: str) -> Optional[List]:
        """Get table schema"""
        try:
            table = self.client.get_table(f"{self.project_id}.{self.dataset_id}.{table_id}")
            return table.schema
        except Exception as e:
            logger_bigquery.error(f"Error retrieving schema for {table_id}: {str(e)}")
            return None
