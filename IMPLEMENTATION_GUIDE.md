"""
COMPREHENSIVE IMPLEMENTATION & EXECUTION GUIDE
Sales Demand Forecasting & Business Intelligence Dashboard
Production-Ready Data Engineering Pipeline

Last Updated: June 2026
Version: 1.0
"""

# ============================================================================
# PART 1: PROJECT OVERVIEW & ARCHITECTURE
# ============================================================================

"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    PROJECT ARCHITECTURE OVERVIEW                          ║
╚════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────┐
│ INPUT: Enterprise Requirements                                         │
├─────────────────────────────────────────────────────────────────────────┤
│ • Historical sales data analysis across 3-year period                  │
│ • Demand forecasting with 87% accuracy target (MAPE)                  │
│ • Customer segmentation for targeted marketing                         │
│ • Executive-level BI dashboard with 3 strategic tabs                  │
│ • Automated daily refresh cycle                                        │
└─────────────────────────────────────────────────────────────────────────┘

                                    ↓↓↓

┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: DATA INGESTION & TRANSFORMATION                               │
├─────────────────────────────────────────────────────────────────────────┤
│ • Synthetic Data Generation (50K+ records)                             │
│ • Data Quality Validation                                              │
│ • ETL Pipeline with Branching Logic                                   │
│ • Load to Google BigQuery                                              │
│                                                                         │
│ Output: transactions table in BigQuery                                 │
│ Records: 50,000+                                                       │
│ Time Range: 3 years (with seasonal patterns)                           │
│ Categories: 12 product types                                           │
│ Customers: ~5,000 unique                                               │
└─────────────────────────────────────────────────────────────────────────┘

                                    ↓↓↓

┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: CUSTOMER INTELLIGENCE & SEGMENTATION                          │
├─────────────────────────────────────────────────────────────────────────┤
│ • RFM Metrics Calculation                                              │
│   - Recency: Days since last purchase                                 │
│   - Frequency: Number of transactions                                  │
│   - Monetary: Total customer lifetime value                            │
│                                                                         │
│ • BigQuery ML K-Means Clustering                                       │
│   - Number of clusters: K=5                                            │
│   - Automatic feature standardization                                  │
│   - Cluster interpretation & business labels                           │
│                                                                         │
│ Output: customer_segments table with assignments                       │
│ Segment Types: VIP_ACTIVE, HIGH_VALUE, STANDARD, AT_RISK, etc.       │
│ Business Value: 15%-40% revenue concentration in top clusters          │
└─────────────────────────────────────────────────────────────────────────┘

                                    ↓↓↓

┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: DEMAND FORECASTING & MODEL EVALUATION                         │
├─────────────────────────────────────────────────────────────────────────┤
│ For each of 12 product categories:                                      │
│                                                                         │
│ Model 1: Facebook Prophet                                              │
│   • 3-year historical training data                                    │
│   • Weekly & yearly seasonality                                        │
│   • Automatic trend detection                                          │
│   • 90-day forecast with confidence intervals                          │
│   • Expected MAPE: 8-12% (~90% accuracy)                              │
│                                                                         │
│ Model 2: ARIMA(1,1,1) Baseline                                         │
│   • Auto-regressive integrated moving average                          │
│   • 7-day seasonal order (ARIMA(1,1,1,7))                             │
│   • Comparison metric for ensemble decisions                           │
│   • Expected MAPE: 12-15% (~85-88% accuracy)                          │
│                                                                         │
│ Evaluation Metrics:                                                     │
│   • MAPE (Mean Absolute Percentage Error)                              │
│   • RMSE (Root Mean Squared Error)                                     │
│   • MAE (Mean Absolute Error)                                          │
│   • Accuracy = 1 - MAPE                                                │
│                                                                         │
│ Output: demand_forecast table with 90-day projections                  │
│ Models Stored: Serialized Prophet & ARIMA objects                      │
│ Accuracy Target: 87% (Target MAPE: 0.13)                              │
└─────────────────────────────────────────────────────────────────────────┘

                                    ↓↓↓

┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 4: BUSINESS INTELLIGENCE DASHBOARD ARCHITECTURE                  │
├─────────────────────────────────────────────────────────────────────────┤
│ Looker Studio 3-Tab Interactive Dashboard:                             │
│                                                                         │
│ TAB 1: Executive Revenue Trends                                         │
│   ✓ KPI Cards (Revenue YTD, Daily Avg, Forecast Accuracy)              │
│   ✓ Historical vs. Forecasted Revenue (Combo Chart)                    │
│   ✓ Category Performance Table (Last 30 days)                          │
│   ✓ Month-over-Month Growth Sparklines                                 │
│   Purpose: Strategic revenue monitoring & forecast accuracy            │
│                                                                         │
│ TAB 2: Inventory Risk Alerts                                            │
│   ✓ Risk Assessment Cards (At-Risk Categories, Demand Gap)             │
│   ✓ Inventory Risk Heatmap (Days of Coverage by Category)              │
│   ✓ Demand vs. Inventory Forecast Chart                                │
│   ✓ Risk Trends for Top 5 Categories                                   │
│   Purpose: Prevent stockouts, optimize inventory planning              │
│                                                                         │
│ TAB 3: Customer Segmentation & Targeting                                │
│   ✓ Segmentation Overview (Cluster Distribution)                       │
│   ✓ Cluster Profile Table (RFM Metrics by Segment)                    │
│   ✓ Top 10 High-Value Customers by Cluster                             │
│   ✓ RFM Score Heatmap (Recency, Frequency, Monetary Ratings)          │
│   Purpose: Targeted marketing, customer retention strategy             │
│                                                                         │
│ Global Features:                                                        │
│   • Date range controls & filters                                      │
│   • Auto-refresh every 4 hours                                         │
│   • Performance optimized for < 10s query times                        │
│   • Drill-down capabilities for analysis                               │
│                                                                         │
│ Output: Live Looker Studio Dashboard                                   │
│ Stakeholders: C-Level, Sales, Inventory Management, Marketing          │
└─────────────────────────────────────────────────────────────────────────┘

                                    ↓↓↓

┌─────────────────────────────────────────────────────────────────────────┐
│ OUTPUT: Integrated Intelligence System                                 │
├─────────────────────────────────────────────────────────────────────────┤
│ 1. BigQuery Data Warehouse                                             │
│    - 6 tables with proper schema & partitioning                        │
│    - Daily automated refresh                                           │
│    - Query optimization & cost management                              │
│                                                                         │
│ 2. Forecasting Models                                                   │
│    - Prophet & ARIMA trained on historical data                        │
│    - 90-day forward forecasts available                                │
│    - Accuracy metrics tracked continuously                             │
│                                                                         │
│ 3. Customer Intelligence                                                │
│    - 5 distinct customer segments identified                           │
│    - RFM scores & business labels assigned                             │
│    - Targeting strategies ready for implementation                     │
│                                                                         │
│ 4. Executive Dashboard                                                  │
│    - Real-time KPI monitoring                                          │
│    - Strategic decision support                                        │
│    - Automated daily updates                                           │
│                                                                         │
│ Business Value Delivered:                                              │
│ • Prevent $XXk in lost revenue from stockouts (inventory optimization) │
│ • Improve marketing ROI by 20-30% (customer targeting)                │
│ • Enable data-driven pricing & promotion strategies (forecasting)     │
│ • Reduce demand planning cycle time by 50% (automation)               │
└─────────────────────────────────────────────────────────────────────────┘
"""

# ============================================================================
# PART 2: STEP-BY-STEP EXECUTION GUIDE
# ============================================================================

"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                  EXECUTION GUIDE - 10 SIMPLE STEPS                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

STEP 1: ENVIRONMENT SETUP
────────────────────────────────────────────────────────────────────────────

1a. Install Python 3.8+
    • Windows: https://www.python.org/downloads/
    • macOS: brew install python3
    • Linux: apt-get install python3 python3-pip

1b. Verify Python installation
    $ python --version          # Should be 3.8+
    $ pip --version             # Should be latest

1c. Navigate to project directory
    $ cd sales-forecasting-project

1d. Create virtual environment
    $ python -m venv venv
    
1e. Activate virtual environment
    # Windows:
    $ venv\\Scripts\\activate
    # macOS/Linux:
    $ source venv/bin/activate


STEP 2: GOOGLE CLOUD PLATFORM (GCP) SETUP
────────────────────────────────────────────────────────────────────────────

2a. Create GCP Account (if needed)
    • Go to: https://cloud.google.com/
    • Click "Try for free"
    • Set up billing account

2b. Create GCP Project
    • Go to: https://console.cloud.google.com/projectcreate
    • Project name: "sales-forecasting"
    • Create

2c. Enable BigQuery API
    • Go to: https://console.cloud.google.com/apis/library
    • Search for "BigQuery API"
    • Click "Enable"

2d. Create Service Account & Download Key
    • Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
    • Click "Create Service Account"
    • Name: "sales-forecasting-sa"
    • Grant roles:
      * BigQuery Admin (or BigQuery Data Editor + ML Admin)
    • Create & Download JSON key
    • Save key file: Keep this file safe!

2e. Note your Project ID
    • Go to: https://console.cloud.google.com/projectselector
    • Copy your Project ID (format: project-123456)


STEP 3: CONFIGURE CREDENTIALS
────────────────────────────────────────────────────────────────────────────

3a. Set environment variable (method 1 - temporary)
    # Windows (PowerShell):
    $env:GOOGLE_APPLICATION_CREDENTIALS="C:\\Users\\YourName\\Downloads\\key.json"
    
    # Windows (Command Prompt):
    set GOOGLE_APPLICATION_CREDENTIALS=C:\\Users\\YourName\\Downloads\\key.json
    
    # macOS/Linux (Bash/Zsh):
    export GOOGLE_APPLICATION_CREDENTIALS="/Users/YourName/Downloads/key.json"

3b. Set environment variable (method 2 - permanent)
    # Create .env file in project root:
    GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
    GCP_PROJECT_ID=your-project-id

3c. Verify credentials
    $ gcloud auth application-default print-access-token
    # Should print a token (not an error)


STEP 4: INSTALL PYTHON DEPENDENCIES
────────────────────────────────────────────────────────────────────────────

4a. Upgrade pip
    $ pip install --upgrade pip

4b. Install project dependencies
    $ pip install -r requirements.txt
    
4c. If Prophet fails on Windows
    # Option A: Install build tools
    # Download: https://visualstudio.microsoft.com/downloads/
    # Select "Desktop development with C++"
    
    # Option B: Use Conda
    $ conda install -c conda-forge fbprophet

4d. Verify installations
    $ python -c "import google.cloud.bigquery; print('✓ BigQuery OK')"
    $ python -c "import prophet; print('✓ Prophet OK')"
    $ python -c "import statsmodels; print('✓ Statsmodels OK')"


STEP 5: CONFIGURE PROJECT SETTINGS
────────────────────────────────────────────────────────────────────────────

5a. Edit config/config.py
    • Open file: config/config.py
    • Update lines 28-29:
      GCP_PROJECT_ID = "your-project-id"        # From Step 2e
      GCP_DATASET_ID = "sales_forecasting_db"   # Or your preference
    
    • Other settings (optional):
      NUM_SYNTHETIC_RECORDS = 50000
      FORECAST_HORIZON_DAYS = 90
      KMEANS_NUM_CLUSTERS = 5
      TARGET_MAPE = 0.87

5b. Verify settings
    $ python -c "from config.config import GCP_PROJECT_ID; print(GCP_PROJECT_ID)"
    # Should print your project ID


STEP 6: RUN DATA SYNTHESIS & ETL (PHASE 1)
────────────────────────────────────────────────────────────────────────────

6a. Run Phase 1
    $ python main.py 1
    
    Execution time: ~2-5 minutes
    
6b. Monitor execution
    • Watch console output for progress
    • Check logs: tail -f logs/etl_pipeline.log
    
6c. Expected results
    • 50,000 synthetic transaction records generated
    • Data loaded to BigQuery transactions table
    • Sample data exported to output/sample_transactions.csv
    
6d. Verify in BigQuery
    $ bq ls -d                              # List datasets
    $ bq ls -t sales_forecasting_db         # List tables
    $ bq query --legacy=false "\\
        SELECT COUNT(*) as total FROM sales_forecasting_db.transactions"


STEP 7: RUN CUSTOMER SEGMENTATION (PHASE 2)
────────────────────────────────────────────────────────────────────────────

7a. Run Phase 2
    $ python main.py 2
    
    Execution time: ~5-10 minutes
    
7b. Monitor execution
    • Watch for cluster training progress
    • Check: logs/customer_segmentation.log
    
7c. Expected results
    • RFM features calculated (rfm_features table)
    • K-Means model trained (customer_segmentation_kmeans)
    • Cluster predictions (customer_segments table)
    • Cluster profiles and insights displayed
    
7d. Verify in BigQuery
    $ bq query --legacy=false "\\
        SELECT assigned_cluster, COUNT(*) as count \\
        FROM sales_forecasting_db.customer_segments \\
        GROUP BY assigned_cluster"


STEP 8: RUN TIME-SERIES FORECASTING (PHASE 3)
────────────────────────────────────────────────────────────────────────────

8a. Run Phase 3
    $ python main.py 3
    
    Execution time: ~10-15 minutes (model training)
    
8b. Monitor execution
    • Watch for Prophet & ARIMA training progress
    • Check: logs/demand_forecasting.log
    • Monitor accuracy metrics vs. 87% target
    
8c. Expected results
    • Prophet models trained (one per category)
    • ARIMA models trained (baseline)
    • 90-day forecasts generated
    • Accuracy metrics reported per category
    
8d. Verify in BigQuery
    $ bq query --legacy=false "\\
        SELECT product_category, COUNT(*) as forecast_days, \\
               AVG(forecasted_revenue) as avg_daily_forecast \\
        FROM sales_forecasting_db.demand_forecast \\
        GROUP BY product_category"


STEP 9: GENERATE DASHBOARD BLUEPRINT (PHASE 4)
────────────────────────────────────────────────────────────────────────────

9a. Run Phase 4
    $ python main.py 4
    
    Execution time: < 1 minute
    
9b. Blueprint generated
    • Output file: output/Looker_Studio_Complete_Blueprint.md
    • Contains complete specifications for all 3 dashboard tabs
    
9c. Review blueprint
    $ cat output/Looker_Studio_Complete_Blueprint.md
    # Or open in text editor / Markdown viewer


STEP 10: BUILD LOOKER STUDIO DASHBOARD
────────────────────────────────────────────────────────────────────────────

10a. Access Looker Studio
     • Go to: https://lookerstudio.google.com
     • Sign in with Google account

10b. Create new report
     • Click "Create" → "Report"
     • Name: "Sales Forecasting Dashboard"

10c. Add BigQuery data source
     • Click "Create new data source"
     • Select "BigQuery"
     • Authorize GCP account
     • Select project → dataset → table

10d. Build Tab 1: Executive Revenue Trends
     • Add 4 KPI cards (Revenue YTD, Daily Avg, Forecast Accuracy, Gap)
     • Add combo chart: Historical vs. Forecasted Revenue
     • Add table: Category Performance
     • Add sparklines: MoM Growth
     • Reference: Blueprint section "TAB 1"

10e. Build Tab 2: Inventory Risk Alerts
     • Add 4 alert cards (At-Risk Categories, Demand Gap, etc.)
     • Add heatmap table: Risk Assessment
     • Add chart: Demand vs. Inventory
     • Reference: Blueprint section "TAB 2"

10f. Build Tab 3: Customer Segmentation
     • Add pie chart: Customer Distribution by Cluster
     • Add table: Cluster Profiles
     • Add table: Top 10 High-Value Customers
     • Add heatmap: RFM Scores
     • Reference: Blueprint section "TAB 3"

10g. Add global controls
     • Date range picker
     • Category filter (dropdown)
     • Segment filter (dropdown)

10h. Configure styling & sharing
     • Apply color palette (Ref: Blueprint "GLOBAL DASHBOARD FEATURES")
     • Share with stakeholders
     • Set refresh schedule to daily

10i. Verify dashboard
     • All charts load correctly
     • Filters work as expected
     • Query performance < 10 seconds


STEP 11: SET UP AUTOMATION (OPTIONAL)
────────────────────────────────────────────────────────────────────────────

11a. Create BigQuery scheduled queries
     • Go to: https://console.cloud.google.com/bigquery
     • Click "Scheduled queries"
     • Create daily refresh for key tables

11b. Set up monitoring
     • Monitor forecast accuracy daily
     • Alert if MAPE exceeds 15% (too high)
     • Alert if data is > 1 day stale

11c. Regular maintenance
     • Review cluster distributions monthly
     • Retrain models quarterly
     • Archive historical forecasts

"""

# ============================================================================
# PART 3: EXPECTED OUTCOMES & SUCCESS CRITERIA
# ============================================================================

"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                   EXPECTED OUTCOMES & SUCCESS CRITERIA                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

PHASE 1: DATA SYNTHESIS & ETL
──────────────────────────────────────────────────────────────────────────

✓ Success Criteria:
  • 50,000+ transaction records generated
  • Data contains all required fields (Transaction_ID, Date, Category, etc.)
  • 3-year date range with realistic patterns
  • 12 distinct product categories
  • ~5,000 unique customers
  • Seasonal trends visible (higher sales in Nov/Dec)
  • Data quality validation passes
  • All records successfully loaded to BigQuery
  • ETL pipeline completes without errors

Sample Output:
  Records generated: 50,000
  Date range: 2023-06-XX to 2026-06-XX
  Unique customers: 4,987
  Total revenue: $12,345,678.90
  Data quality: ✓ PASSED


PHASE 2: CUSTOMER SEGMENTATION
──────────────────────────────────────────────────────────────────────────

✓ Success Criteria:
  • RFM metrics calculated for all customers
  • K=5 clusters created via BigQuery ML
  • Each customer assigned to exactly one cluster
  • Cluster profiles make business sense
  • High-value segment identified
  • At-risk segment identified
  • Average monetary value differs significantly by cluster

Sample Output:
  Clusters created: 5
  Model training status: ✓ Complete
  Cluster 0 (High-Value): 800 customers, Avg LTV $2,500
  Cluster 1 (Standard): 2,100 customers, Avg LTV $500
  Cluster 2 (One-Time): 1,200 customers, Avg LTV $100
  RFM correlation: 0.92 (strong)


PHASE 3: DEMAND FORECASTING
──────────────────────────────────────────────────────────────────────────

✓ Success Criteria:
  • Prophet models trained for all 12 categories
  • ARIMA baseline models trained
  • 90-day forecast generated for each category
  • Forecast accuracy >= 85% (ideally > 87%)
  • MAPE reported for each model
  • Confidence intervals provided
  • Models serialize successfully
  • Evaluation on test set completes

Sample Output - Prophet Results:
  Category: Electronics
  MAPE: 0.089 (8.9% error, 91.1% accuracy) ✓
  RMSE: $1,234.56
  90-day forecast: Starting at $45,678/day, trending up

  Category: Apparel
  MAPE: 0.115 (11.5% error, 88.5% accuracy) ✓
  RMSE: $567.89
  90-day forecast: Seasonal, peak in Dec

  Average Accuracy: 89.2% ✓ EXCEEDS TARGET (87%)


PHASE 4: LOOKER STUDIO DASHBOARD
──────────────────────────────────────────────────────────────────────────

✓ Success Criteria - Tab 1 (Revenue Trends):
  • Revenue YTD KPI displays correctly
  • Historical vs. Forecast chart shows data
  • Revenue trend is visible (up/down)
  • Category performance table loads
  • All queries complete in < 10 seconds
  • MoM growth sparklines display

✓ Success Criteria - Tab 2 (Inventory Risk):
  • Risk alert cards display key metrics
  • Heatmap shows risk distribution
  • At-risk categories identified
  • Demand-Supply gap visible
  • No stockout warnings for well-stocked items

✓ Success Criteria - Tab 3 (Customer Segmentation):
  • Cluster distribution pie chart shows 5 clusters
  • Cluster profile table displays RFM metrics
  • High-value customers clearly identified
  • Top 10 customers shown with LTV values
  • RFM heatmap color-coded by score

✓ Global Dashboard Features:
  • Date filter works correctly
  • Category filter filters all charts
  • Dashboard loads in < 5 seconds
  • Refresh button works
  • Mobile-responsive layout

"""

# ============================================================================
# PART 4: TROUBLESHOOTING & COMMON ISSUES
# ============================================================================

"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                       TROUBLESHOOTING GUIDE                            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

ISSUE 1: "ModuleNotFoundError: No module named 'google.cloud'"
────────────────────────────────────────────────────────────────────────────
Cause: google-cloud-bigquery not installed
Solution:
  $ pip install --upgrade google-cloud-bigquery
  $ python -c "import google.cloud.bigquery; print('OK')"


ISSUE 2: "PermissionError: Could not authenticate with Google Cloud"
────────────────────────────────────────────────────────────────────────────
Cause: Credentials not set or invalid
Solution:
  1. Verify GOOGLE_APPLICATION_CREDENTIALS path exists
  2. Check credentials file is valid JSON
  3. Service account has BigQuery permissions
  4. Credentials haven't expired
  
  Test:
  $ python -c "
  from google.oauth2 import service_account
  creds = service_account.Credentials.from_service_account_file('key.json')
  print('✓ Credentials valid')
  "


ISSUE 3: "DatasetNotFound: 404 Not found: Dataset your-project:dataset"
────────────────────────────────────────────────────────────────────────────
Cause: Dataset doesn't exist or wrong project ID
Solution:
  1. Verify GCP_PROJECT_ID in config.py is correct
  2. Dataset will be created automatically on first run
  3. If not created:
     $ bq mk --dataset --location=US sales_forecasting_db


ISSUE 4: "Prophet fails with 'ModuleNotFoundError: No module named 'pystan'"
────────────────────────────────────────────────────────────────────────────
Cause: Prophet dependencies not installed (Windows issue)
Solution Option A (use conda):
  $ conda create -n forecasting python=3.10
  $ conda activate forecasting
  $ conda install -c conda-forge fbprophet

Solution Option B (install C++ build tools):
  Download: https://visualstudio.microsoft.com/downloads/
  Select "Desktop development with C++"
  Install and retry

Solution Option C (pre-built wheel):
  $ pip install pystan==2.19.1.1
  $ pip install fbprophet


ISSUE 5: "Forecast accuracy below 87% target"
────────────────────────────────────────────────────────────────────────────
Cause: Model hyperparameters not optimal
Solution:
  # In config/config.py, try:
  PROPHET_SEASONALITY_MODE = "multiplicative"  # vs "additive"
  PROPHET_YEARLY_SEASONALITY = True
  PROPHET_WEEKLY_SEASONALITY = True
  
  # Or use ensemble:
  forecast = (prophet_forecast + arima_forecast) / 2
  
  # Or collect more historical data (> 3 years)


ISSUE 6: "BigQuery query timeout after 300 seconds"
────────────────────────────────────────────────────────────────────────────
Cause: Large dataset or inefficient query
Solution:
  1. Use daily_sales_aggregated (pre-aggregated) instead of transactions
  2. Add date filters to queries
  3. Use partitioned tables
  4. Break into smaller queries


ISSUE 7: "Out of memory during data generation"
────────────────────────────────────────────────────────────────────────────
Cause: NUM_SYNTHETIC_RECORDS too large for available RAM
Solution:
  # In config/config.py, reduce:
  NUM_SYNTHETIC_RECORDS = 25000  # Instead of 50000
  
  # Or increase available memory
  # Process data in batches (see code comments)


ISSUE 8: "Looker Studio shows 'Data source error'"
────────────────────────────────────────────────────────────────────────────
Cause: BigQuery data source connection lost or credentials expired
Solution:
  1. Refresh data source in Looker Studio
  2. Re-authorize BigQuery connection
  3. Verify table names in queries
  4. Check BigQuery dataset has data


ISSUE 9: "Cluster predictions show all customers in one cluster"
────────────────────────────────────────────────────────────────────────────
Cause: Features not properly standardized or K too large
Solution:
  # In config/config.py, try:
  KMEANS_NUM_CLUSTERS = 3  # Reduce from 5
  
  # Or verify RFM features are calculated:
  $ bq query "SELECT * FROM dataset.rfm_features LIMIT 10"


ISSUE 10: "Dashboard filters not working"
────────────────────────────────────────────────────────────────────────────
Cause: Filter dimensions not properly linked to data
Solution:
  1. Verify data source has filter column
  2. Link filter to correct data source
  3. Use correct column name (case-sensitive)
  4. Test with single chart first


GENERAL DEBUGGING:
────────────────────────────────────────────────────────────────────────────
1. Check logs:
   $ tail -f logs/etl_pipeline.log
   $ tail -f logs/forecasting.log

2. Verify credentials:
   $ gcloud auth application-default print-access-token

3. Test BigQuery connection:
   $ bq ls  # List datasets
   $ bq show project_id:dataset_id  # Show dataset info

4. Enable logging verbosity:
   # In config/logging_config.py
   LOG_LEVEL = "DEBUG"  # More detailed logs

"""

# ============================================================================
# END OF COMPREHENSIVE IMPLEMENTATION GUIDE
# ============================================================================

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                   IMPLEMENTATION GUIDE - REFERENCE                        ║
    ║          Sales Demand Forecasting & Business Intelligence Dashboard      ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    
    This file contains:
    1. Complete project architecture overview
    2. Step-by-step execution guide (10 simple steps)
    3. Expected outcomes & success criteria
    4. Comprehensive troubleshooting guide
    
    START HERE:
    1. Read PART 1 for architecture understanding
    2. Follow PART 2 (Steps 1-11) sequentially
    3. Verify outcomes against PART 3
    4. Use PART 4 for any issues
    
    Files to review:
    • README.md - Complete documentation
    • QUICKSTART.md - 5-minute quick start
    • config/config.py - Configuration parameters
    • main.py - Main orchestrator script
    
    Execute with:
    $ python main.py              # Run all phases
    $ python main.py 1 2 3 4      # Specific phases
    
    Happy Forecasting! 🚀
    """)
