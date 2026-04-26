# 📊 Strategic HR Data Pipeline & Analytics Platform

## 🔗 Live Dashboard
👉 https://hty-hr-data-pipeline-analytics.streamlit.app/
## 🔗 Data Source
👉 https://www.kaggle.com/datasets/rhuebner/human-resources-data-set

---

## 🚀 Project Overview

This project demonstrates a **production-style HR data pipeline**, simulating how real companies process, transform, and analyze employee data.

It implements a full **ELT (Extract–Load–Transform)** workflow with:

- Cloud Data Warehouse (TiDB)
- SQL-based transformations (Medallion Architecture)
- Automated pipelines (GitHub Actions)
- Real-time analytics dashboard (Streamlit)

---

## 🧠 Key Engineering Concepts

### ✔ Medallion Architecture (Why it matters)

| Layer | Purpose |
|------|--------|
| Bronze | Preserve raw data (no data loss) |
| Silver | Clean & standardize data |
| Gold | Serve business-ready analytics |

👉 This design ensures:
- Data traceability
- Reproducibility
- Scalable analytics

---

## 🔄 Data Flow (End-to-End)

```text
CSV Dataset
   ↓
Python Ingestion (SQLAlchemy)
   ↓
TiDB Cloud (Bronze Table)
   ↓
SQL Transformations (Silver → Gold)
   ↓
Streamlit Dashboard (Real-time Query)
   ↓
GitHub Actions (Daily Automation)
````

---

## ⚙️ Pipeline Details

### 1️⃣ Data Ingestion

📄 `ingest_tidb.py` 

* Loads CSV into TiDB
* Uses SQLAlchemy
* Handles special characters in credentials

⚠️ Design Choice:

* Raw table uses `VARCHAR` for flexibility
* Prevents schema mismatch during ingestion

---

### 2️⃣ Data Transformation

📄 `run_sql_pipeline.py` 

* Executes SQL scripts sequentially
* Implements ELT approach

Transformations include:

* Data type casting
* Tenure calculation
* Salary normalization
* Attrition flag creation

---

### 3️⃣ Automation (CI/CD)

📄 `.github/workflows/pipeline.yml`

* Runs daily (cron job)
* Executes SQL pipeline automatically

👉 Result:

* Dashboard always reflects latest data
* No manual intervention needed

---

## 📊 Dashboard Features

📄 `app.py` 

### 🏠 Company Overview

* Headcount tracking
* Salary & tenure insights

### 📉 Attrition Analysis

* Root cause breakdown
* High-risk tenure periods

### 🔍 Recruitment Analytics

* Channel performance comparison
* Retention & satisfaction metrics

### 💰 Pay Equity Analysis

* Detects:

  * Underpaid Veterans (High Risk)
  * Rising Stars
  * Overpaid Newcomers

---

## 🧪 Real-World Engineering Challenges Solved

✔ Dirty data handling (dates, salary formats)
✔ Schema flexibility (VARCHAR → typed transformation)
✔ Automated pipeline execution
✔ Separation of storage vs analytics layers
✔ Real-time dashboard integration

---

## 📦 Tech Stack

| Category        | Tools             |
| --------------- | ----------------- |
| Database        | TiDB Cloud        |
| Data Processing | SQL               |
| Backend         | Python            |
| Visualization   | Streamlit, Plotly |
| Automation      | GitHub Actions    |

---

## 🚀 Deployment

* **Database**: TiDB Cloud
* **Dashboard**: Streamlit Cloud
* **Automation**: GitHub Actions

---

## 📈 Future Improvements

* Incremental data loading (CDC)
* Data validation (Great Expectations)
* Airflow orchestration
* Machine learning (attrition prediction)