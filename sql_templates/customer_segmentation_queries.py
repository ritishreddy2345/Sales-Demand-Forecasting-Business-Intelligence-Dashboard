"""
PHASE 2: SQL Templates for Customer Segmentation using BigQuery ML
Includes RFM calculation, K-Means clustering, and prediction queries
"""

# ============================================================================
# QUERY 1: Create RFM Feature Table
# ============================================================================
CREATE_RFM_FEATURES_QUERY = """
-- Create RFM (Recency, Frequency, Monetary) features for customer segmentation
CREATE OR REPLACE TABLE `{project_id}.{dataset_id}.{rfm_table}` AS
SELECT
    customer_id,
    
    -- RECENCY: Days since last purchase
    DATE_DIFF(CURRENT_DATE(), MAX(transaction_date), DAY) AS recency_days,
    
    -- FREQUENCY: Number of transactions
    COUNT(DISTINCT transaction_id) AS frequency_purchases,
    
    -- MONETARY: Total spending
    ROUND(SUM(total_revenue), 2) AS monetary_value,
    
    -- Additional features for segmentation
    COUNT(DISTINCT DATE(transaction_date)) AS unique_purchase_days,
    ROUND(AVG(total_revenue), 2) AS avg_transaction_value,
    ROUND(MAX(total_revenue), 2) AS max_transaction_value,
    ROUND(MIN(total_revenue), 2) AS min_transaction_value,
    COUNT(DISTINCT product_category) AS distinct_categories_purchased,
    ROUND(SUM(quantity_sold), 2) AS total_quantity_purchased,
    
    -- RFM Score calculation (simplified 1-5 scale)
    CASE 
        WHEN DATE_DIFF(CURRENT_DATE(), MAX(transaction_date), DAY) <= 30 THEN 5
        WHEN DATE_DIFF(CURRENT_DATE(), MAX(transaction_date), DAY) <= 60 THEN 4
        WHEN DATE_DIFF(CURRENT_DATE(), MAX(transaction_date), DAY) <= 90 THEN 3
        WHEN DATE_DIFF(CURRENT_DATE(), MAX(transaction_date), DAY) <= 180 THEN 2
        ELSE 1
    END AS recency_score,
    
    CASE 
        WHEN COUNT(DISTINCT transaction_id) >= 50 THEN 5
        WHEN COUNT(DISTINCT transaction_id) >= 30 THEN 4
        WHEN COUNT(DISTINCT transaction_id) >= 15 THEN 3
        WHEN COUNT(DISTINCT transaction_id) >= 5 THEN 2
        ELSE 1
    END AS frequency_score,
    
    CASE 
        WHEN SUM(total_revenue) >= 10000 THEN 5
        WHEN SUM(total_revenue) >= 5000 THEN 4
        WHEN SUM(total_revenue) >= 2000 THEN 3
        WHEN SUM(total_revenue) >= 500 THEN 2
        ELSE 1
    END AS monetary_score,
    
    -- Segment label (optional - for reference)
    CASE 
        WHEN DATE_DIFF(CURRENT_DATE(), MAX(transaction_date), DAY) <= 30 
             AND SUM(total_revenue) >= 5000 THEN 'VIP_ACTIVE'
        WHEN SUM(total_revenue) >= 10000 THEN 'HIGH_VALUE'
        WHEN DATE_DIFF(CURRENT_DATE(), MAX(transaction_date), DAY) > 180 THEN 'DORMANT'
        ELSE 'STANDARD'
    END AS segment_label,
    
    CURRENT_TIMESTAMP() AS calculation_timestamp

FROM `{project_id}.{dataset_id}.{transactions_table}`
WHERE transaction_date IS NOT NULL
GROUP BY customer_id
ORDER BY monetary_value DESC
"""


# ============================================================================
# QUERY 2: Create K-Means Clustering Model
# ============================================================================
CREATE_KMEANS_MODEL_QUERY = """
-- Create BigQuery ML K-Means clustering model for customer segmentation
-- This model will identify natural customer groupings based on RFM features
CREATE OR REPLACE MODEL `{project_id}.{dataset_id}.{model_name}` OPTIONS(
    model_type='linear_reg',
    model_type='kmeans',
    num_clusters={num_clusters},
    standardize_features=true,
    max_iterations={max_iterations},
    initialization_method='{init_method}',
    kmeans_initialization_column=null
) AS
SELECT
    -- Feature scaling: BigQuery ML handles standardization
    -- Input features for clustering
    CAST(recency_days AS FLOAT64) as recency,
    CAST(frequency_purchases AS FLOAT64) as frequency,
    CAST(monetary_value AS FLOAT64) as monetary_value,
    CAST(avg_transaction_value AS FLOAT64) as avg_order_value,
    CAST(distinct_categories_purchased AS FLOAT64) as category_diversity,
    CAST(total_quantity_purchased AS FLOAT64) as total_quantity,
    
    -- Derived features
    CAST(unique_purchase_days AS FLOAT64) as purchase_frequency_days,
    CASE WHEN monetary_value > 0 THEN frequency_purchases / NULLIF(unique_purchase_days, 0) ELSE 0 END as purchase_velocity
    
FROM `{project_id}.{dataset_id}.{rfm_table}`
WHERE 
    recency_days IS NOT NULL
    AND frequency_purchases IS NOT NULL
    AND monetary_value IS NOT NULL
    AND monetary_value > 0  -- Only customers with purchases
"""


# ============================================================================
# QUERY 3: Predict Customer Clusters
# ============================================================================
PREDICT_CLUSTERS_QUERY = """
-- Predict clusters for all customers
-- This query assigns each customer to a cluster and calculates distance to centroid
SELECT
    rf.customer_id,
    rf.recency_days,
    rf.frequency_purchases,
    rf.monetary_value,
    rf.avg_transaction_value,
    rf.distinct_categories_purchased,
    rf.total_quantity_purchased,
    rf.unique_purchase_days,
    rf.segment_label,
    
    -- Cluster assignment
    p.centroid_id AS assigned_cluster,
    p.nearest_centroid_distance AS distance_to_cluster_center,
    
    -- Calculate distance from customer to centroid as percentage
    ROUND(100 * (p.nearest_centroid_distance / MAX(p.nearest_centroid_distance) OVER ()), 2) AS distance_percentile,
    
    -- Business interpretation of cluster
    CASE p.centroid_id
        WHEN 0 THEN 'Cluster_0'
        WHEN 1 THEN 'Cluster_1'
        WHEN 2 THEN 'Cluster_2'
        WHEN 3 THEN 'Cluster_3'
        WHEN 4 THEN 'Cluster_4'
        ELSE 'Other_Cluster'
    END AS cluster_name,
    
    CURRENT_TIMESTAMP() AS prediction_timestamp

FROM `{project_id}.{dataset_id}.{rfm_table}` rf
LEFT JOIN ML.PREDICT(
    MODEL `{project_id}.{dataset_id}.{model_name}`,
    (
        SELECT
            rf.customer_id,
            CAST(rf.recency_days AS FLOAT64) as recency,
            CAST(rf.frequency_purchases AS FLOAT64) as frequency,
            CAST(rf.monetary_value AS FLOAT64) as monetary_value,
            CAST(rf.avg_transaction_value AS FLOAT64) as avg_order_value,
            CAST(rf.distinct_categories_purchased AS FLOAT64) as category_diversity,
            CAST(rf.total_quantity_purchased AS FLOAT64) as total_quantity,
            CAST(rf.unique_purchase_days AS FLOAT64) as purchase_frequency_days,
            CASE WHEN rf.monetary_value > 0 THEN rf.frequency_purchases / NULLIF(rf.unique_purchase_days, 0) ELSE 0 END as purchase_velocity
        FROM `{project_id}.{dataset_id}.{rfm_table}` rf
    )
) p
ON rf.customer_id = p.customer_id
ORDER BY assigned_cluster, distance_to_cluster_center ASC
"""


# ============================================================================
# QUERY 4: Cluster Summary Statistics
# ============================================================================
CLUSTER_SUMMARY_QUERY = """
-- Generate summary statistics for each cluster
SELECT
    assigned_cluster,
    cluster_name,
    COUNT(DISTINCT customer_id) AS num_customers,
    ROUND(AVG(recency_days), 1) AS avg_recency_days,
    ROUND(AVG(frequency_purchases), 1) AS avg_frequency,
    ROUND(AVG(monetary_value), 2) AS avg_monetary_value,
    ROUND(AVG(avg_transaction_value), 2) AS avg_order_value,
    ROUND(AVG(distinct_categories_purchased), 1) AS avg_categories,
    ROUND(MIN(monetary_value), 2) AS min_monetary_value,
    ROUND(MAX(monetary_value), 2) AS max_monetary_value,
    ROUND(STDDEV(monetary_value), 2) AS stddev_monetary_value,
    
    -- Business metrics per cluster
    ROUND(SUM(total_quantity_purchased), 0) AS total_quantity_sold,
    COUNT(DISTINCT customer_id) / SUM(COUNT(DISTINCT customer_id)) OVER () * 100 AS pct_of_customers,
    
    -- Cluster interpretation
    CASE 
        WHEN AVG(monetary_value) > (SELECT PERCENTILE_CONT(monetary_value, 0.75) FROM `{project_id}.{dataset_id}.{predictions_table}`)
             AND AVG(recency_days) < 60 THEN 'PREMIUM_ACTIVE'
        WHEN AVG(monetary_value) > (SELECT PERCENTILE_CONT(monetary_value, 0.5) FROM `{project_id}.{dataset_id}.{predictions_table}`)
             THEN 'HIGH_VALUE'
        WHEN AVG(recency_days) > 180 THEN 'AT_RISK_DORMANT'
        WHEN AVG(frequency_purchases) < 5 THEN 'ONE_TIME_BUYERS'
        ELSE 'STANDARD'
    END AS cluster_interpretation
    
FROM `{project_id}.{dataset_id}.{predictions_table}`
WHERE assigned_cluster IS NOT NULL
GROUP BY assigned_cluster, cluster_name
ORDER BY avg_monetary_value DESC
"""


# ============================================================================
# QUERY 5: Top Customers by Cluster (for targeting)
# ============================================================================
TOP_CUSTOMERS_BY_CLUSTER_QUERY = """
-- Identify top 10 high-value customers in each cluster for targeted campaigns
SELECT
    assigned_cluster,
    cluster_name,
    customer_id,
    monetary_value,
    frequency_purchases,
    recency_days,
    avg_transaction_value,
    distinct_categories_purchased,
    segment_label,
    ROW_NUMBER() OVER (PARTITION BY assigned_cluster ORDER BY monetary_value DESC) AS rank_in_cluster
    
FROM `{project_id}.{dataset_id}.{predictions_table}`
WHERE assigned_cluster IS NOT NULL
QUALIFY rank_in_cluster <= 10
ORDER BY assigned_cluster, rank_in_cluster
"""


# ============================================================================
# Export variables for use in Python scripts
# ============================================================================
SQL_QUERIES = {
    'create_rfm_features': CREATE_RFM_FEATURES_QUERY,
    'create_kmeans_model': CREATE_KMEANS_MODEL_QUERY,
    'predict_clusters': PREDICT_CLUSTERS_QUERY,
    'cluster_summary': CLUSTER_SUMMARY_QUERY,
    'top_customers_by_cluster': TOP_CUSTOMERS_BY_CLUSTER_QUERY
}
