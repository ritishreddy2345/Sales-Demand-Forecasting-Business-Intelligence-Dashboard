# 🚀 Testing & Run Guide
## Sales Demand Forecasting & BI Dashboard Project

---

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [Environment Setup](#environment-setup)
3. [Running the Full Pipeline](#running-the-full-pipeline)
4. [Testing Individual Phases](#testing-individual-phases)
5. [Troubleshooting](#troubleshooting)
6. [Validation Checklist](#validation-checklist)

---

## Quick Start

### Prerequisites
- Python 3.8+ installed
- Windows PowerShell (or bash for Unix)
- GCP Project with BigQuery enabled (**required for full pipeline**)
- Service Account JSON key for GCP (**required for full pipeline**)

### 5-Minute Setup (Local Testing)
```powershell
cd "C:\Users\HP\AppData\Local\Temp\Sales-Demand-Forecasting-Business-Intelligence-Dashboard"

# Activate virtual environment
.\venv\Scripts\activate.ps1

# Verify core packages installed
python -c "import pandas, numpy, google.cloud.bigquery; print('✓ Core packages OK')"
```

---

## Environment Setup

### Step 1: Virtual Environment (✓ ALREADY CREATED)
```powershell
# Virtual environment already exists at: ./venv
.\venv\Scripts\activate.ps1
```

### Step 2: Install Dependencies
```powershell
# Install from cleaned requirements.txt
pip install -r requirements.txt

# Or install manually if requirements.txt has issues:
pip install google-cloud-bigquery==3.13.0 pandas==2.1.3 numpy==1.26.2
pip install statsmodels==0.14.0 scikit-learn==1.3.2 scipy==1.11.4
pip install python-dotenv==1.0.0
# Optional (Prophet may require MS C++ Build Tools on Windows):
pip install fbprophet==0.7.10
```

### Step 3: Set Up GCP Credentials

**Option A: Service Account JSON Key** (Recommended)
```powershell
# Windows PowerShell
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\your\service-account-key.json"

# Verify authentication
python -c "from google.cloud import bigquery; client = bigquery.Client(); print(f'✓ Connected to project: {client.project}')"
```

**Option B: Application Default Credentials**
```powershell
# Using gcloud CLI (install gcloud SDK first)
gcloud auth application-default login
```

### Step 4: Update Configuration
Edit `config/config.py`:
```python
GCP_PROJECT_ID = "your-gcp-project-id"  # Replace with your project
GCP_DATASET_ID = "sales_forecasting_db"  # Name of your BigQuery dataset
BIGQUERY_REGION = "US"  # Adjust if needed
```

---

## Running the Full Pipeline

### Complete End-to-End Execution
```powershell
.\venv\Scripts\activate.ps1
python main.py
```

**Expected Output:**
```
====================================================================================================
                    PHASE 1: DATA SYNTHESIS & ETL PIPELINE TO BIGQUERY
====================================================================================================

🚀 Generating 50,000 synthetic transaction records...
✓ Synthetic data generated successfully
✓ Data uploaded to BigQuery

====================================================================================================
                    PHASE 2: CUSTOMER SEGMENTATION USING BIGQUERY ML
====================================================================================================

✓ RFM features calculated
✓ K-Means model trained
✓ Clusters assigned

====================================================================================================
                    PHASE 3: TIME-SERIES DEMAND FORECASTING
====================================================================================================

✓ Daily sales aggregated
✓ Prophet model trained
✓ ARIMA model trained
✓ 90-day forecasts generated

====================================================================================================
                         PROJECT EXECUTION SUMMARY
====================================================================================================
Phase 1: SUCCESS
Phase 2: SUCCESS  
Phase 3: SUCCESS
Total Runtime: XX minutes
```

---

## Testing Individual Phases

### Test Phase 1: Data Synthesis & ETL
```powershell
.\venv\Scripts\activate.ps1

# Test data synthesis only (generates 10K records locally)
python -c "
from src.phase1_etl.data_synthesis import DataSynthesis
ds = DataSynthesis(num_records=10000)
df = ds.generate_synthetic_data()
print(f'✓ Generated {len(df)} records')
print(df.head())
"
```

**Expected Output:**
```
✓ Generated 10000 records
  Transaction_ID    Date Product_Category  Customer_ID  Quantity_Sold  Unit_Price  Total_Revenue
0           TXN001 2023-01-01   Electronics        CUST001              5        89.99      449.95
1           TXN002 2023-01-01       Apparel        CUST005              3        29.99       89.97
...
```

---

### Test Phase 2: Customer Segmentation (Requires BigQuery)
```powershell
.\venv\Scripts\activate.ps1

python -c "
from src.phase2_segmentation.customer_segmentation import CustomerSegmentation
cs = CustomerSegmentation()
success = cs.run_segmentation_pipeline()
print(f'✓ Segmentation Pipeline: {\"SUCCESS\" if success else \"FAILED\"}')
"
```

**Expected Output:**
```
✓ RFM features table created
✓ K-Means model created/trained
✓ Cluster predictions generated
✓ Segmentation Pipeline: SUCCESS
```

---

### Test Phase 3: Time-Series Forecasting
```powershell
.\venv\Scripts\activate.ps1

python -c "
from src.phase3_forecasting.demand_forecasting import DemandForecasting
df = DemandForecasting()
success = df.run_forecasting_pipeline()
print(f'✓ Forecasting Pipeline: {\"SUCCESS\" if success else \"FAILED\"}')
"
```

**Expected Output:**
```
✓ Daily sales data extracted
✓ Prophet model trained
✓ ARIMA model trained
✓ 90-day forecasts generated
✓ MAPE calculated: XX.X%
✓ Forecasting Pipeline: SUCCESS
```

---

## Validation Checklist

### ✅ Pre-Run Validation
- [ ] Python 3.8+ installed: `python --version`
- [ ] Virtual environment activated: Check for `(venv)` in terminal prompt
- [ ] Dependencies installed: `pip list | grep -E "pandas|numpy|google-cloud"`
- [ ] GCP credentials set: Check `$env:GOOGLE_APPLICATION_CREDENTIALS` is set
- [ ] BigQuery connection verified: Run `python -c "from google.cloud import bigquery; bigquery.Client()"`

### ✅ Post-Run Validation
- [ ] BigQuery dataset created with tables:
  - `transactions`
  - `rfm_features`
  - `customer_segments`
  - `daily_sales_aggregated`
  - `demand_forecast`

- [ ] Output files generated:
  - `output/synthetic_data_sample.csv` (50K records)
  - `output/customer_segments.csv` (customer cluster assignments)
  - `output/demand_forecast_90days.csv` (forecast predictions)
  - `output/forecast_metrics.json` (MAPE, accuracy scores)

- [ ] Forecast accuracy achieved:
  - Prophet MAPE: ~87% or better
  - ARIMA MAPE: ~85% or better

### ✅ Performance Benchmarks
| Phase | Expected Duration | Status |
|-------|-------------------|--------|
| Phase 1: Data Synthesis & ETL | 2-5 minutes | ⏳ |
| Phase 2: Segmentation | 3-7 minutes | ⏳ |
| Phase 3: Forecasting | 5-10 minutes | ⏳ |
| **Total Pipeline** | **~15-25 minutes** | ⏳ |

---

## Troubleshooting

### Issue 1: `ModuleNotFoundError: No module named 'google.cloud'`
**Solution:**
```powershell
pip install google-cloud-bigquery
```

### Issue 2: `GOOGLE_APPLICATION_CREDENTIALS not found`
**Solution:**
```powershell
# Check if credentials are set
echo $env:GOOGLE_APPLICATION_CREDENTIALS

# Set credentials (if not set)
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\service-account-key.json"

# Verify file exists
Test-Path "C:\path\to\service-account-key.json"
```

### Issue 3: Authentication Error from BigQuery
**Solution:**
```powershell
# Re-authenticate with gcloud
gcloud auth application-default login

# Or set service account credentials
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\key.json"
```

### Issue 4: `fbprophet` Installation Fails on Windows
**Solution:**
```powershell
# Option A: Use conda instead
conda install -c conda-forge fbprophet

# Option B: Install Microsoft C++ Build Tools first, then:
pip install fbprophet

# Option C: Skip Prophet, use ARIMA only (remove fbprophet from requirements)
```

### Issue 5: Out of Memory or Slow Processing
**Solution:**
```powershell
# Reduce synthetic record count in config.py:
NUM_SYNTHETIC_RECORDS = 10000  # Instead of 50000

# Run a single phase only:
python -c "from src.phase1_etl.etl_pipeline import ETLPipeline; ETLPipeline().run_etl_pipeline()"
```

### Issue 6: BigQuery Table Already Exists Error
**Solution:**
```powershell
# Option A: Allow upsert (script handles this automatically)
# Option B: Delete table in BigQuery and re-run:
bq rm -t sales_forecasting_db.transactions  # or any table name
```

---

## Advanced Testing

### Run with Custom Parameters
```powershell
.\venv\Scripts\activate.ps1

# Generate smaller dataset for faster testing
python -c "
import os
os.environ['NUM_SYNTHETIC_RECORDS'] = '5000'
from main import ProjectOrchestrator
orchestrator = ProjectOrchestrator()
orchestrator.run_phase_1_etl()
"
```

### Verify Data Quality
```powershell
.\venv\Scripts\activate.ps1

python -c "
import pandas as pd
from src.phase1_etl.data_synthesis import DataSynthesis

# Generate data
ds = DataSynthesis(num_records=1000)
df = ds.generate_synthetic_data()

# Validate
print(f'Total Records: {len(df)}')
print(f'Date Range: {df[\"Date\"].min()} to {df[\"Date\"].max()}')
print(f'Unique Categories: {df[\"Product_Category\"].nunique()}')
print(f'Unique Customers: {df[\"Customer_ID\"].nunique()}')
print(f'Total Revenue: \${df[\"Total_Revenue\"].sum():,.2f}')
print(f'Missing Values:\n{df.isnull().sum()}')
"
```

---

## Logs & Debugging

### View Application Logs
```powershell
# Logs are stored in ./logs/ directory
Get-Content -Path "logs\sales_forecasting.log" -Tail 50

# Or stream logs in real-time
Get-Content -Path "logs\sales_forecasting.log" -Wait
```

### Enable Debug Logging
```powershell
# In config/config.py or via environment:
$env:LOG_LEVEL = "DEBUG"
python main.py
```

---

## Next Steps After Testing

1. **Connect Looker Studio Dashboard:**
   - Connect to BigQuery dataset `sales_forecasting_db`
   - Add data sources for tables: `demand_forecast`, `customer_segments`
   - See DASHBOARD_BLUEPRINT.md for design guidelines

2. **Automate Pipeline:**
   - Set up scheduled queries in BigQuery
   - Use Cloud Scheduler for daily data ingestion

3. **Monitor Performance:**
   - Track forecast accuracy over time
   - Analyze forecast drift
   - Retrain models monthly with new data

4. **Scale to Production:**
   - Deploy to Cloud Run for automated execution
   - Set up monitoring and alerts
   - Implement CI/CD pipeline

---

## Support & Documentation

- 📖 See [README.md](README.md) for project overview
- 📊 See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for architecture details
- 🛠️ See [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) for technical deep-dive
- 📋 See [DELIVERY_MANIFEST.md](DELIVERY_MANIFEST.md) for deliverables checklist

---

**Last Updated:** 2026-06-07  
**Project Status:** Production-Ready ✅
