![dbt models](https://img.shields.io/badge/dbt-models-green)
![Luigi Pipeline](https://img.shields.io/badge/luigi-scheduled-blue)
![MLflow Tracking](https://img.shields.io/badge/mlflow-logging-orange)
![Streamlit Dashboard](https://img.shields.io/badge/streamlit-live-red)
![License](https://img.shields.io/badge/license-MIT-lightgrey)


# 🩺 ChronicCare Analytics Platform

A fully simulated analytics + ML platform for remote health monitoring, wellness coaching, and chronic condition management.

## 🚀 Overview

This project is designed for industries focused on personalized care, digital wellness programs, and remote health analytics. It combines real-time biometric data, health coaching session outcomes, and AI alert tracking to deliver insights into user engagement, risk prediction, and program effectiveness.

---

## 🎯 Ideal Use Cases

This architecture applies to:
- Digital health & wellness platforms
- Chronic care management programs
- Remote behavioral coaching or therapy
- Corporate wellness and employee health benefit tools
- Population health analytics & predictive modeling

---

## 📂 Project Structure

| Component     | Description |
|---------------|-------------|
| `data/`       | Simulated CSVs: users, device logs, sessions, alerts, ML |
| `models/`     | dbt models (staging + marts) for analytics |
| `dashboards/` | Streamlit app for cohort and outcome tracking |
| `ml/`         | PyTorch dropout risk model with MLflow logging |
| `orchestration/` | Luigi pipeline to run dbt + ML |
| `docs/`       | ERD, metadata, portfolio visuals |

---

## 🔬 Key Features

- Cohort-based chronic condition segmentation
- Session outcome tracking (NPS, effectiveness)
- Real-time biometric and behavioral engagement metrics
- AI alert classification and resolution
- ML-based disengagement risk modeling
- MLOps via MLflow (with PyTorch model)
- Luigi for pipeline orchestration and automation

---

## 🧪 Getting Started

1. `pip install -r requirements.txt`
2. Run full pipeline:  
   `luigi --module orchestration.pipeline FullPipeline --local-scheduler`
3. Launch dashboard:  
   `streamlit run dashboards/app.py`

Built for healthcare and wellness data engineering portfolios, interviews, and real-world prototypes.

---

