# QUICK START GUIDE
# Sales Demand Forecasting & BI Dashboard Project

## 🚀 5-MINUTE SETUP

### Step 1: Prerequisites
- Python 3.8+
- GCP Account with BigQuery access

### Step 2: Clone and Setup
```bash
cd sales-forecasting-project
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 3: Install & Configure
```bash
pip install -r requirements.txt

# Set GCP credentials
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\key.json"  # Windows
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"  # macOS/Linux
```

### Step 4: Update config/config.py
```python
GCP_PROJECT_ID = "your-project-id"
GCP_DATASET_ID = "sales_forecasting_db"
```

### Step 5: Run Pipeline
```bash
python main.py
```

---

## 📊 What Gets Created

✓ 50,000 synthetic transaction records  
✓ 5,000 unique customer profiles  
✓ 3 years of historical data  
✓ Customer segmentation clusters (K=5)  
✓ 90-day demand forecasts by category  
✓ Forecast accuracy metrics  
✓ Looker Studio dashboard blueprint  

---

## 🎯 Expected Output

### BigQuery Tables:
- `transactions` - 50K+ records
- `daily_sales_aggregated` - Daily totals by category
- `customer_segments` - Cluster assignments with RFM
- `rfm_features` - Customer-level RFM metrics
- `demand_forecast` - 90-day forecasts
- `forecast_models_metrics` - Model evaluation results

### Files:
- `output/sample_transactions.csv` - Sample data preview
- `output/Looker_Studio_Complete_Blueprint.md` - Dashboard specs
- `logs/etl_pipeline.log` - ETL execution log
- `logs/forecasting.log` - Forecast model log

---

## 🔍 Verify Installation

```bash
# Test BigQuery connection
python -c "from src.bigquery_utils import BigQueryManager; print('✓ BigQuery OK')"

# Test Prophet
python -c "from prophet import Prophet; print('✓ Prophet OK')"

# Test ARIMA
python -c "from statsmodels.tsa.arima.model import ARIMA; print('✓ ARIMA OK')"

# Test data generation
python -c "from src.phase1_etl.data_synthesis import SyntheticDataGenerator; print('✓ Data Gen OK')"
```

---

## ❓ Common Issues

### "ModuleNotFoundError: No module named 'google.cloud'"
```bash
pip install --upgrade google-cloud-bigquery
```

### "Prophet import error on Windows"
```bash
# Use conda instead:
conda install -c conda-forge fbprophet
```

### "403 Forbidden - BigQuery access denied"
- Check service account has BigQuery Admin role
- Check credentials file path in GOOGLE_APPLICATION_CREDENTIALS

### "Dataset not found"
- Verify GCP_PROJECT_ID in config.py
- Ensure BigQuery dataset exists or is created automatically

---

## 📈 Next Steps

After running `python main.py`:

1. **Review Output**
   ```bash
   # Check logs
   cat logs/etl_pipeline.log
   cat logs/forecasting.log
   
   # View sample data
   cat output/sample_transactions.csv
   ```

2. **Build Looker Studio Dashboard**
   - Open `output/Looker_Studio_Complete_Blueprint.md`
   - Go to https://lookerstudio.google.com
   - Connect BigQuery datasets
   - Follow blueprint to create 3 tabs

3. **Verify Results in BigQuery**
   ```sql
   SELECT COUNT(*) FROM project.dataset.transactions;
   SELECT DISTINCT assigned_cluster FROM project.dataset.customer_segments;
   SELECT COUNT(*) FROM project.dataset.demand_forecast;
   ```

4. **Run Individual Phases**
   ```bash
   python main.py 1              # Phase 1 only
   python main.py 1 2            # Phases 1-2
   python main.py 3              # Phase 3 only
   ```

---

## 📚 Full Documentation

See README.md for:
- Complete project architecture
- Detailed phase explanations
- Configuration reference
- SQL templates
- Troubleshooting guide
- Best practices

---

## 💬 Support

- Check logs in `logs/` directory
- Review output in `output/` directory
- Consult README.md for troubleshooting
- Check `config/config.py` for settings

---

**Ready? Run: `python main.py` 🚀**
