![dbt models](https://img.shields.io/badge/dbt-models-green)
![Luigi Pipeline](https://img.shields.io/badge/luigi-scheduled-blue)
![MLflow Tracking](https://img.shields.io/badge/mlflow-logging-orange)
![Streamlit Dashboard](https://img.shields.io/badge/streamlit-live-red)


# 🩺 ChronicCare Analytics Platform

A fully simulated analytics + ML platform for remote health monitoring, wellness coaching, and chronic condition management with comprehensive patient engagement tracking and AI-driven health insights.

## 🚀 Overview

This project demonstrates a comprehensive healthcare analytics ecosystem designed for industries focused on personalized care, digital wellness programs, and remote health analytics. It combines patient engagement data, clinical session outcomes, and AI alert tracking to deliver insights into user behavior, risk prediction, and program effectiveness for chronic condition management.

---

## 🎯 Ideal Use Cases

This architecture applies to:
- **Digital health & wellness platforms** with chronic condition management
- **Remote patient monitoring** programs with engagement analytics
- **Chronic care management** with predictive risk modeling
- **Telehealth platforms** with session outcome tracking
- **Corporate wellness** and employee health benefit programs
- **Population health analytics** & predictive modeling
- **Healthcare coaching** platforms with behavioral insights

---

## 📂 Project Structure

| Component | Description |
|-----------|-------------|
| `data/` | **Sample datasets**: users, engagement metrics, clinical sessions, AI alerts |
| `dashboard/` | **Streamlit analytics app**: Multi-tab dashboard for chronic care insights |
| `models/` | dbt models (staging + marts) for analytics transformation |
| `ml/` | PyTorch dropout risk model with MLflow experiment tracking |
| `orchestration/` | Luigi pipeline orchestration for automated data processing |
| `docs/` | ERD diagrams, data dictionary, and portfolio documentation |

---

## 🔬 Key Features

### 📈 Analytics & Insights
- **Cohort-based chronic condition segmentation** (Diabetes, Hypertension, Heart Disease, Asthma)
- **Patient engagement tracking** with behavioral analytics and dropout risk modeling
- **Clinical session outcome analysis** with NPS scores and effectiveness metrics
- **AI alert management** with resolution tracking and severity analysis

### 🤖 AI & Machine Learning
- **ML-based disengagement risk scoring** with continuous patient monitoring
- **Predictive analytics** for identifying at-risk patients
- **Alert classification system** with automated severity-based routing
- **Behavioral pattern recognition** for personalized care recommendations

### 🏗️ Technical Architecture
- **Interactive dashboards** built with Streamlit and Plotly
- **MLOps integration** via MLflow experiment tracking
- **Pipeline orchestration** with Luigi for automated workflows
- **Scalable data processing** with pandas and numpy

---

## 🧪 Getting Started

### Prerequisites
```bash
pip install streamlit pandas plotly numpy pathlib
```

### Quick Setup
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd chroniccare-analytics
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch ChronicCare Analytics Dashboard**
   ```bash
   streamlit run dashboard/app.py
   ```

### Full Pipeline Execution
```bash
# Run complete data pipeline
luigi --module orchestration.pipeline FullPipeline --local-scheduler

# Train ML models
python ml/train_dropout_model.py

# Launch dashboard
streamlit run dashboard/app.py
```

---

## 📊 Sample Data Overview

### 🏥 Dataset Structure
| File | Records | Description |
|------|---------|-------------|
| `users.csv` | 25 patients | Demographics, conditions, registration data |
| `ml_engagement_training_data.csv` | 40+ records | Daily activity, app usage, dropout risk scores |
| `clinical_sessions.csv` | 38 sessions | Virtual/in-person visits with outcome tracking |
| `ai_alerts.csv` | 43 alerts | ML-generated health alerts with resolution status |

### 🎯 Data Characteristics
- **Patient Demographics**: 25 users across 4 chronic conditions (Diabetes, Hypertension, Heart Disease, Asthma)
- **Engagement Metrics**: Daily steps (3,800-9,400), app usage (0.9-3.6 hrs), medication adherence
- **Risk Stratification**: Dropout risk scores (0.13-0.92) for predictive modeling
- **Clinical Outcomes**: NPS scores (2-10), session effectiveness (4.2-9.5)
- **Alert Diversity**: 7 alert types with realistic resolution patterns (~70% resolved)

---

## 🔧 Dashboard Features

### 📊 Dashboard Overview
- **Key Performance Indicators**: Total users, active engagement, session metrics
- **Population Analytics**: User distribution by condition and demographics
- **Engagement Summaries**: Average steps, NPS scores, alert resolution rates
- **Condition-Based Insights**: Performance metrics segmented by chronic conditions

### 👥 User Engagement
- **Activity Analytics**: Daily steps distribution and engagement patterns
- **Dropout Risk Analysis**: ML-powered risk segmentation with visual categorization
- **Behavioral Insights**: Engagement metrics by medical condition
- **Trend Analysis**: Activity and risk patterns over time

### 🩺 Clinical Sessions
- **Session Outcomes**: Effectiveness scores by session type (Virtual, In-Person, Telehealth, Emergency)
- **Patient Satisfaction**: NPS score tracking and provider performance
- **Utilization Trends**: Daily session volume and temporal patterns
- **Provider Analytics**: Session distribution across healthcare providers

### 🚨 AI Alerts
- **Alert Management**: Resolution rates by alert type and severity
- **Performance Monitoring**: Alert volume trends and response times
- **Risk Prioritization**: Critical vs. routine alert distribution
- **Condition Correlation**: Alert patterns by patient medical conditions

---

## 🎛️ Interactive Filtering

### Available Filters
- **Medical Condition**: Diabetes, Hypertension, Heart Disease, Asthma
- **Patient Demographics**: Gender-based segmentation
- **Alert Types**: Medication Adherence, Vitals Anomalies, Activity Patterns
- **Date Ranges**: Customizable time windows for trend analysis

### Dynamic Analytics
- **Real-time KPI updates** based on filter selections
- **Cross-tab analysis** between conditions and outcomes
- **Temporal trend visualization** with interactive charts
- **Drill-down capabilities** from population to individual insights

---

## 🔍 Advanced Analytics Features

### Machine Learning Integration
- **Dropout Risk Modeling**: Continuous risk scoring for patient retention
- **Engagement Prediction**: Behavioral pattern analysis for intervention timing
- **Alert Prioritization**: ML-driven severity classification and routing

### Clinical Decision Support
- **Risk Stratification**: Automated patient segmentation for care planning
- **Outcome Prediction**: Session effectiveness forecasting
- **Resource Optimization**: Provider allocation based on patient needs

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/analytics-enhancement`)
3. Commit your changes (`git commit -am 'Add new analytics feature'`)
4. Push to the branch (`git push origin feature/analytics-enhancement`)
5. Create a Pull Request

---

Built for healthcare analytics portfolios, demonstrating end-to-end data pipeline capabilities with ML integration and interactive business intelligence for chronic care management.
