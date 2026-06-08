# ⚡ QUICK COMMAND REFERENCE CARD

**Print this page or bookmark it for quick reference!**

---

## 🚀 FAST START (Copy & Paste)

### Test Locally (No GCP needed)
```powershell
cd "C:\Users\HP\AppData\Local\Temp\Sales-Demand-Forecasting-Business-Intelligence-Dashboard"
.\venv\Scripts\activate.ps1
python test_local_validation.py
```
**Time:** 3-5 minutes | **Result:** ✅ 5/5 tests pass

---

### Run Full Pipeline (Requires GCP)
```powershell
# 1. Set credentials
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\key.json"

# 2. Run pipeline
python main.py
```
**Time:** 20-30 minutes | **Result:** Data in BigQuery + forecasts

---

## 📋 COMMON COMMANDS

### Activate Virtual Environment
```powershell
.\venv\Scripts\activate.ps1
```
Check: Terminal shows `(venv)` prefix ✓

---

### Verify Packages Installed
```powershell
pip list | Select-String "pandas|numpy|bigquery|statsmodels"
```

---

### Test Data Synthesis Only
```powershell
python -c "
from src.phase1_etl.data_synthesis import SyntheticDataGenerator
gen = SyntheticDataGenerator()
df = gen.generate_transactions(5000)
print(f'Generated {len(df):,} records')
print(f'Revenue: \${df[\"total_revenue\"].sum():,.0f}')
"
```

---

### View Recent Logs
```powershell
Get-Content logs\etl_pipeline.log -Tail 50
```

---

### Test BigQuery Connection
```powershell
python -c "
from google.cloud import bigquery
client = bigquery.Client()
print(f'✓ Project: {client.project}')
"
```

---

### Run Individual Phases

**Phase 1 Only:**
```powershell
python -c "
from src.phase1_etl.etl_pipeline import ETLPipeline
ETLPipeline().run_etl_pipeline(generate_new_data=True)
"
```

**Phase 2 Only:**
```powershell
python -c "
from src.phase2_segmentation.customer_segmentation import CustomerSegmentation
CustomerSegmentation().run_segmentation_pipeline()
"
```

**Phase 3 Only:**
```powershell
python -c "
from src.phase3_forecasting.demand_forecasting import DemandForecasting
DemandForecasting().run_forecasting_pipeline()
"
```

---

## 🔐 GCP SETUP

### Set Credentials Variable
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\Users\HP\AppData\Local\Temp\my-project-key.json"
```

### Make Credentials Permanent (Session)
```powershell
[Environment]::SetEnvironmentVariable("GOOGLE_APPLICATION_CREDENTIALS","C:\path\to\key.json","Process")
```

### Verify Credentials Set
```powershell
echo $env:GOOGLE_APPLICATION_CREDENTIALS
```

---

## ⚙️ CONFIGURATION UPDATES

### Edit Configuration File
```powershell
notepad config\config.py
```

### Key Settings to Update
```python
# Line 26
GCP_PROJECT_ID = "your-actual-project-id"

# Line 27
GCP_DATASET_ID = "sales_forecasting_db"

# Line 52 (optional)
NUM_SYNTHETIC_RECORDS = 10000  # Reduce for faster testing
```

---

## 📊 OUTPUT EXPLORATION

### List Generated Files
```powershell
Get-ChildItem output\ | Select-Object Name, Length
```

### Preview CSV Data
```powershell
python -c "
import pandas as pd
df = pd.read_csv('output/synthetic_data_sample.csv', nrows=5)
print(df)
"
```

### Check Forecast Results
```powershell
python -c "
import pandas as pd
df = pd.read_csv('output/demand_forecast_90days.csv')
print(f'Forecasted {len(df)} days')
print(f'Accuracy: {df[\"mape\"].mean():.1f}%')
"
```

---

## 🔍 DEBUGGING

### Check Python Version
```powershell
python --version
```

### Check Virtual Environment Active
```powershell
python -c "import sys; print(sys.prefix)"
```

### Show All Installed Packages
```powershell
pip list
```

### Check Package Version
```powershell
pip show google-cloud-bigquery
```

### Reinstall Package
```powershell
pip uninstall google-cloud-bigquery -y
pip install google-cloud-bigquery==3.41.0
```

---

## 📁 FILE LOCATIONS

### Project Root
```
C:\Users\HP\AppData\Local\Temp\Sales-Demand-Forecasting-Business-Intelligence-Dashboard
```

### Important Files
```
config/config.py              # Configuration (EDIT THIS)
main.py                       # Main orchestrator
test_local_validation.py      # Run tests
requirements.txt              # Dependencies
```

### Output Directories
```
output/                       # Generated CSV files
logs/                         # Execution logs
```

---

## 📖 QUICK DOCUMENTATION MAP

| Task | File |
|------|------|
| Get started | QUICK_START_RUN_NOW.md |
| Verify setup | VERIFICATION_CHECKLIST.md |
| Troubleshoot | TESTING_AND_RUN_GUIDE.md |
| Full details | README.md |
| This reference | QUICK_COMMAND_REFERENCE.md |

---

## ✅ VERIFICATION COMMANDS

```powershell
# 1. Environment OK?
python --version

# 2. Packages OK?
python -c "import pandas, numpy, statsmodels; print('✓ OK')"

# 3. BigQuery OK?
python -c "from google.cloud import bigquery; print('✓ OK')"

# 4. Config OK?
python -c "from config.config import GCP_PROJECT_ID; print(f'Project: {GCP_PROJECT_ID}')"

# 5. Data synthesis OK?
python -c "from src.phase1_etl.data_synthesis import SyntheticDataGenerator; print('✓ OK')"

# All tests OK?
python test_local_validation.py
```

---

## 🎯 COMMON WORKFLOWS

### Workflow 1: Local Testing (5 min)
```powershell
.\venv\Scripts\activate.ps1
python test_local_validation.py
# Result: ✅ 5/5 tests pass
```

### Workflow 2: Generate Sample Data (2 min)
```powershell
.\venv\Scripts\activate.ps1
python -c "
from src.phase1_etl.data_synthesis import SyntheticDataGenerator
gen = SyntheticDataGenerator()
df = gen.generate_transactions(1000)
df.to_csv('sample_data.csv', index=False)
print(f'✓ Saved 1,000 records')
"
```

### Workflow 3: Run Full Pipeline (25 min)
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\key.json"
.\venv\Scripts\activate.ps1
python main.py
# Result: Data in BigQuery + forecasts generated
```

### Workflow 4: Check Results (2 min)
```powershell
python -c "
import pandas as pd
import os
print('Output files:')
for f in os.listdir('output'):
    size = os.path.getsize(f'output/{f}')
    print(f'  {f}: {size/1024:.1f} KB')
"
```

---

## 🚨 ERROR RECOVERY

### Clear Cache & Reinstall
```powershell
pip cache purge
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Reset Virtual Environment
```powershell
Remove-Item venv -Recurse -Force
python -m venv venv
.\venv\Scripts\activate.ps1
pip install -r requirements.txt
```

### Clear Output & Logs
```powershell
Remove-Item output\* -Force
Remove-Item logs\* -Force
```

---

## ⏱️ TIMING REFERENCE

| Task | Time |
|------|------|
| Activate venv | < 1 sec |
| Local validation tests | 3-5 min |
| Generate 10K records | 2-3 min |
| Generate 50K records | 5-10 min |
| Phase 2 Segmentation | 3-5 min |
| Phase 3 Forecasting | 5-10 min |
| Full pipeline | 20-30 min |

---

## 🔗 ENVIRONMENT VARIABLES

### Set for Current Session
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = "path/to/key.json"
$env:LOG_LEVEL = "DEBUG"
```

### View Current Values
```powershell
echo $env:GOOGLE_APPLICATION_CREDENTIALS
echo $env:LOG_LEVEL
```

### Clear Variable
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = $null
```

---

## 💾 PACKAGE MANAGEMENT

### Show All Packages
```powershell
pip list
```

### Install Single Package
```powershell
pip install pandas==2.1.3
```

### Upgrade Specific Package
```powershell
pip install --upgrade google-cloud-bigquery
```

### Check for Updates
```powershell
pip list --outdated
```

---

## 📝 USEFUL ONE-LINERS

### Count Records in CSV
```powershell
@(Get-Content output/synthetic_data_sample.csv | Measure-Object -Line).Lines - 1
```

### Show First 5 Lines
```powershell
Get-Content output/synthetic_data_sample.csv | Select-Object -First 5
```

### Get File Size
```powershell
(Get-Item output/synthetic_data_sample.csv).Length / 1MB
```

### Show Recent Log Entries
```powershell
Get-Content logs\etl_pipeline.log | Select-Object -Last 20
```

---

## 🎓 LEARNING PATH

1. **Start:** `python test_local_validation.py` (5 min)
2. **Read:** QUICK_START_RUN_NOW.md (10 min)
3. **Setup:** GCP credentials (15 min)
4. **Run:** `python main.py` (25 min)
5. **Explore:** Results in BigQuery (10 min)
6. **Next:** Connect Looker Studio (60 min)

---

## ⚡ MOST USED COMMANDS

```powershell
# Activate environment
.\venv\Scripts\activate.ps1

# Run all tests
python test_local_validation.py

# Run full pipeline
python main.py

# View logs
Get-Content logs\etl_pipeline.log -Tail 50

# Generate test data
python -c "from src.phase1_etl.data_synthesis import SyntheticDataGenerator; SyntheticDataGenerator().generate_transactions(1000).to_csv('test.csv', index=False)"

# Set BigQuery credentials
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\key.json"

# Check packages
pip list | Select-String "pandas|numpy|bigquery"
```

---

## 🆘 HELP RESOURCES

| Issue | Resource |
|-------|----------|
| Can't activate venv | See SETUP_SUMMARY.md |
| Package errors | See TESTING_AND_RUN_GUIDE.md |
| BigQuery errors | See TESTING_AND_RUN_GUIDE.md troubleshooting |
| Configuration | See config/config.py |
| Data exploration | See output/ directory |

---

## ✨ PRO TIPS

1. **Keep terminal open** - Faster testing cycle
2. **Use one-liners** - Copy & paste for quick tests
3. **Check logs first** - Errors appear in logs/ directory
4. **Save this page** - Bookmark for quick reference
5. **Read error messages** - They're usually helpful!

---

**Print & Keep Handy! 📌**

**Last Updated:** 2026-06-07  
**Version:** 1.0 Quick Reference
