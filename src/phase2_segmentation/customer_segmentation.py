"""
PHASE 2: Customer Segmentation using BigQuery ML (K-Means)
Orchestrates RFM feature creation, model training, and prediction
"""

import pandas as pd
from typing import Tuple
from config.logging_config import logger_segmentation
from config.config import (
    GCP_PROJECT_ID,
    GCP_DATASET_ID,
    RFM_FEATURES_TABLE,
    CUSTOMER_SEGMENTS_TABLE,
    TRANSACTIONS_TABLE,
    KMEANS_NUM_CLUSTERS,
    KMEANS_MAX_ITERATIONS,
    KMEANS_INIT_METHOD
)
from src.bigquery_utils import BigQueryManager
from sql_templates.customer_segmentation_queries import SQL_QUERIES


class CustomerSegmentation:
    """Orchestrates customer segmentation using BigQuery ML"""
    
    def __init__(self, project_id: str = GCP_PROJECT_ID):
        """Initialize segmentation manager"""
        self.project_id = project_id
        self.dataset_id = GCP_DATASET_ID
        self.bq_manager = BigQueryManager(project_id)
        self.model_name = "customer_segmentation_kmeans"
        logger_segmentation.info("CustomerSegmentation initialized")
    
    def create_rfm_features(self) -> Tuple[bool, str]:
        """
        Step 1: Create RFM feature table
        Aggregates transaction data into customer-level RFM metrics
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            logger_segmentation.info("=" * 80)
            logger_segmentation.info("STEP 1: CREATING RFM FEATURE TABLE")
            logger_segmentation.info("=" * 80)
            
            # Format query with project and dataset details
            query = SQL_QUERIES['create_rfm_features'].format(
                project_id=self.project_id,
                dataset_id=self.dataset_id,
                rfm_table=RFM_FEATURES_TABLE,
                transactions_table=TRANSACTIONS_TABLE
            )
            
            logger_segmentation.info(f"Creating table: {RFM_FEATURES_TABLE}")
            
            # Execute query
            result_df = self.bq_manager.execute_query(query, timeout_seconds=600)
            
            if result_df is not None:
                msg = f"✓ RFM feature table '{RFM_FEATURES_TABLE}' created successfully"
                logger_segmentation.info(msg)
                
                # Show sample results
                sample_query = f"""
                SELECT TOP 5 * FROM `{self.project_id}.{self.dataset_id}.{RFM_FEATURES_TABLE}`
                ORDER BY monetary_value DESC
                """
                sample_df = self.bq_manager.execute_query(sample_query)
                if sample_df is not None and len(sample_df) > 0:
                    logger_segmentation.info(f"\nSample RFM Features (Top 5 by value):\n{sample_df.to_string()}")
                
                return True, msg
            else:
                msg = f"✗ Failed to create RFM feature table"
                logger_segmentation.error(msg)
                return False, msg
        
        except Exception as e:
            error_msg = f"Error creating RFM features: {str(e)}"
            logger_segmentation.error(error_msg)
            return False, error_msg
    
    def create_kmeans_model(self) -> Tuple[bool, str]:
        """
        Step 2: Create K-Means clustering model
        Trains BigQuery ML model on RFM features
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            logger_segmentation.info("\n" + "=" * 80)
            logger_segmentation.info("STEP 2: CREATING K-MEANS CLUSTERING MODEL")
            logger_segmentation.info("=" * 80)
            
            # Format query with model parameters
            query = SQL_QUERIES['create_kmeans_model'].format(
                project_id=self.project_id,
                dataset_id=self.dataset_id,
                model_name=self.model_name,
                rfm_table=RFM_FEATURES_TABLE,
                num_clusters=KMEANS_NUM_CLUSTERS,
                max_iterations=KMEANS_MAX_ITERATIONS,
                init_method=KMEANS_INIT_METHOD
            )
            
            logger_segmentation.info(f"Model configuration:")
            logger_segmentation.info(f"  - Number of clusters: {KMEANS_NUM_CLUSTERS}")
            logger_segmentation.info(f"  - Max iterations: {KMEANS_MAX_ITERATIONS}")
            logger_segmentation.info(f"  - Initialization method: {KMEANS_INIT_METHOD}")
            logger_segmentation.info(f"\nTraining model: {self.model_name}")
            
            # Note: CREATE MODEL queries don't return traditional results
            # We check if the model was created successfully
            result_df = self.bq_manager.execute_query(query, timeout_seconds=1800)
            
            # Verify model exists
            try:
                self.bq_manager.client.get_model(
                    f"{self.project_id}.{self.dataset_id}.{self.model_name}"
                )
                msg = f"✓ K-Means model '{self.model_name}' created successfully"
                logger_segmentation.info(msg)
                return True, msg
            except:
                msg = f"✗ Failed to verify K-Means model creation"
                logger_segmentation.error(msg)
                return False, msg
        
        except Exception as e:
            error_msg = f"Error creating K-Means model: {str(e)}"
            logger_segmentation.error(error_msg)
            return False, error_msg
    
    def predict_clusters(self) -> Tuple[bool, str]:
        """
        Step 3: Predict customer clusters
        Assigns each customer to a cluster
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            logger_segmentation.info("\n" + "=" * 80)
            logger_segmentation.info("STEP 3: PREDICTING CUSTOMER CLUSTERS")
            logger_segmentation.info("=" * 80)
            
            # Format query
            query = SQL_QUERIES['predict_clusters'].format(
                project_id=self.project_id,
                dataset_id=self.dataset_id,
                rfm_table=RFM_FEATURES_TABLE,
                model_name=self.model_name,
                predictions_table=CUSTOMER_SEGMENTS_TABLE
            )
            
            logger_segmentation.info(f"Creating predictions table: {CUSTOMER_SEGMENTS_TABLE}")
            
            # Execute prediction and create table
            success = self.bq_manager.create_table_from_query(query, CUSTOMER_SEGMENTS_TABLE)
            
            if success:
                msg = f"✓ Customer cluster predictions created successfully"
                logger_segmentation.info(msg)
                
                # Show cluster distribution
                dist_query = f"""
                SELECT 
                    assigned_cluster,
                    COUNT(DISTINCT customer_id) as num_customers,
                    ROUND(AVG(monetary_value), 2) as avg_value,
                    ROUND(MAX(monetary_value), 2) as max_value,
                    ROUND(MIN(monetary_value), 2) as min_value
                FROM `{self.project_id}.{self.dataset_id}.{CUSTOMER_SEGMENTS_TABLE}`
                GROUP BY assigned_cluster
                ORDER BY assigned_cluster
                """
                dist_df = self.bq_manager.execute_query(dist_query)
                if dist_df is not None:
                    logger_segmentation.info(f"\nCluster Distribution:\n{dist_df.to_string()}")
                
                return True, msg
            else:
                msg = f"✗ Failed to create cluster predictions"
                logger_segmentation.error(msg)
                return False, msg
        
        except Exception as e:
            error_msg = f"Error predicting clusters: {str(e)}"
            logger_segmentation.error(error_msg)
            return False, error_msg
    
    def generate_cluster_insights(self) -> Tuple[bool, pd.DataFrame]:
        """
        Step 4: Generate cluster summary statistics
        Provides business insights for each cluster
        
        Returns:
            Tuple of (success: bool, insights_df: DataFrame)
        """
        try:
            logger_segmentation.info("\n" + "=" * 80)
            logger_segmentation.info("STEP 4: GENERATING CLUSTER INSIGHTS")
            logger_segmentation.info("=" * 80)
            
            query = SQL_QUERIES['cluster_summary'].format(
                project_id=self.project_id,
                dataset_id=self.dataset_id,
                predictions_table=CUSTOMER_SEGMENTS_TABLE
            )
            
            insights_df = self.bq_manager.execute_query(query)
            
            if insights_df is not None and len(insights_df) > 0:
                logger_segmentation.info(f"✓ Generated insights for {len(insights_df)} clusters")
                logger_segmentation.info(f"\nCluster Insights:\n{insights_df.to_string()}")
                return True, insights_df
            else:
                logger_segmentation.warning("No insights generated")
                return True, pd.DataFrame()  # Return empty df but still success
        
        except Exception as e:
            error_msg = f"Error generating insights: {str(e)}"
            logger_segmentation.error(error_msg)
            return False, pd.DataFrame()
    
    def run_segmentation_pipeline(self) -> bool:
        """
        Execute complete customer segmentation pipeline
        
        Returns:
            True if successful
        """
        try:
            logger_segmentation.info("\n" + "🎯 " * 20)
            logger_segmentation.info("STARTING CUSTOMER SEGMENTATION PIPELINE")
            logger_segmentation.info("🎯 " * 20 + "\n")
            
            # Step 1: Create RFM features
            success, msg = self.create_rfm_features()
            if not success:
                logger_segmentation.error("RFM feature creation failed. Aborting.")
                return False
            
            # Step 2: Create K-Means model
            success, msg = self.create_kmeans_model()
            if not success:
                logger_segmentation.error("K-Means model creation failed. Aborting.")
                return False
            
            # Step 3: Predict clusters
            success, msg = self.predict_clusters()
            if not success:
                logger_segmentation.error("Cluster prediction failed. Aborting.")
                return False
            
            # Step 4: Generate insights
            success, insights_df = self.generate_cluster_insights()
            if not success:
                logger_segmentation.error("Insight generation failed. Aborting.")
                return False
            
            # Final summary
            logger_segmentation.info("\n" + "✓ " * 20)
            logger_segmentation.info("CUSTOMER SEGMENTATION PIPELINE COMPLETED SUCCESSFULLY")
            logger_segmentation.info("✓ " * 20)
            
            return True
        
        except Exception as e:
            logger_segmentation.error(f"Fatal error in segmentation pipeline: {str(e)}")
            return False


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    import sys
    import time
    
    # Initialize segmentation
    segmentation = CustomerSegmentation()
    
    # Run pipeline
    start_time = time.time()
    success = segmentation.run_segmentation_pipeline()
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 80)
    print("PHASE 2 CUSTOMER SEGMENTATION EXECUTION SUMMARY")
    print("=" * 80)
    print(f"Status: {'✓ SUCCESS' if success else '✗ FAILED'}")
    print(f"Execution time: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
    print("=" * 80)
    
    sys.exit(0 if success else 1)
