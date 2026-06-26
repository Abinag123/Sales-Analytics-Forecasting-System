# Sales-Analytics-Forecasting-System
parses, cleans, and runs analytics on retail transactional databases.

# Sales Analytics & Forecasting System

An end-to-end Python pipeline demonstrating transactional data extraction, ETL preprocessing using Pandas, trend analytics, and moving-average forecasting methods.

---

## 📈 Architecture & Flow

1.  **Ingestion & Ingestion (Extract):** Simulates retail database inputs, generating structured transactional tables.
2.  **ETL Pipelines (Transform):** Cleans anomalies, handles duplicate indexes, reformats datetimes, and calculates revenue fields.
3.  **Statistical Analytics (Load & Analyze):** Conducts sales analysis across product categories and generates monthly aggregation metrics.
4.  **Forecasting Layer:** Computes rolling 3-month moving averages to generate future forecasting baselines for inventory and business management.

---

## 🛠️ Tech Stack
*   Python 3.14
*   Pandas (ETL & Analytical Processing)
*   NumPy (Statistical & Array calculations)
*   OpenPyXL / Excel (Structured data exports)

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install pandas numpy openpyxl
```

### 2. Run Pipeline
```bash
python sales_analytics.py
```
Outputs report summaries directly to the console and exports the finalized structured dataset to `Sales_Analytics_Output.xlsx`.
