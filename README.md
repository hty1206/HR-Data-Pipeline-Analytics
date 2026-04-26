# 📊 HR Data Pipeline & Analytics Dashboard

## 🔗 Live Demo
👉 https://hty-hr-data-pipeline-analytics.streamlit.app/

---

## 📌 Project Overview

This project simulates a **real-world HR data pipeline** from raw data ingestion to a fully automated analytics dashboard.

It demonstrates how to build an end-to-end **ELT pipeline** using:

- Cloud Database (TiDB)
- SQL-based data transformation (Bronze / Silver / Gold)
- Python for ingestion & orchestration
- Streamlit for interactive dashboard
- GitHub Actions for automation

---

## 🏗️ Architecture

```

Raw Data (CSV)
↓
Python Ingestion
↓
Bronze Layer (Raw Table)
↓
Silver Layer (Data Cleaning & Feature Engineering)
↓
Gold Layer (Business Metrics & Aggregations)
↓
Streamlit Dashboard
↓
GitHub Actions (Auto Refresh)

````

---

## 🧱 Data Layers

### 🥉 Bronze Layer
- Table: `hr_raw_data`
- Raw HR dataset
- All fields stored as VARCHAR for ingestion stability

---

### 🥈 Silver Layer
- Table: `hr_employees_silver`
- Data type conversion
- Feature engineering:
  - Tenure calculation
  - Salary normalization
  - Attrition flag

---

### 🥇 Gold Layer (Business Views)

| View | Description |
|------|------------|
| `gold_company_summary` | Company-level KPIs |
| `gold_dept_performance` | Department performance |
| `gold_attrition_detailed` | Attrition analysis |
| `gold_recruitment_quality` | Hiring channel evaluation |
| `gold_pay_equity_analysis` | Salary fairness analysis |

---

## ⚙️ Data Pipeline

### 1. Data Ingestion

Python script uploads raw CSV into TiDB:

📄 `ingest_tidb.py`

- Uses SQLAlchemy
- Connects to TiDB Cloud
- Writes to `hr_raw_data`

```python
df.to_sql('hr_raw_data', if_exists='append')
````

---

### 2. Data Transformation (ELT)

📄 `run_sql_pipeline.py`

Executes SQL scripts:

* Silver transformation
* Gold aggregations

```python
conn.execute(text(cmd))
```

---

### 3. Automation (RPA)

📄 `.github/workflows/pipeline.yml`

* Runs pipeline daily
* Automates:

  * Data ingestion
  * SQL transformation
  * Dashboard update

---

## 📊 Dashboard Features

📄 `app.py`

Built with Streamlit + Plotly

### 🔹 Key Insights

#### 🏠 Company Overview

* Total employees
* Active employees
* Avg salary & tenure

#### 📉 Attrition Analysis

* Why employees leave
* Attrition peak by tenure

#### 🔍 Recruitment Analysis

* Hiring channel performance
* Retention & satisfaction

#### 💰 Pay Equity

* Salary fairness classification
* High-risk employee detection

---

## 🧪 Testing

📄 `testing_insert_update.sql`

Simulates:

* Insert new employees
* Update HR records

---

## 📦 Tech Stack

| Layer           | Tools             |
| --------------- | ----------------- |
| Data Storage    | TiDB Cloud        |
| Data Processing | SQL               |
| Backend         | Python            |
| Visualization   | Streamlit, Plotly |
| Orchestration   | GitHub Actions    |

---

## 🚀 Deployment

* Dashboard: Streamlit Cloud
* Database: TiDB Cloud
* CI/CD: GitHub Actions

---

## 📈 Key Highlights

✔ End-to-end ELT pipeline
✔ Real-time dashboard
✔ Cloud-native architecture
✔ Automated data refresh
✔ Business-driven analytics

---

## 🧠 Future Improvements

* Incremental data ingestion
* Data validation checks
* Airflow orchestration
* User authentication for dashboard