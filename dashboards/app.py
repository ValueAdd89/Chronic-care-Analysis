
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 ChronicCare Analytics Dashboard")

@st.cache_data
def load_data():
    users = pd.read_csv("data/users.csv")
    engagement = pd.read_csv("data/ml_engagement_training_data.csv")
    sessions = pd.read_csv("data/clinical_sessions.csv")
    alerts = pd.read_csv("data/ai_alerts.csv")
    return users, engagement, sessions, alerts

users, engagement, sessions, alerts = load_data()

with st.sidebar:
    st.header("Filters")
    selected_condition = st.selectbox("Condition", options=["All"] + sorted(users['condition'].unique().tolist()))
    if selected_condition != "All":
        users = users[users['condition'] == selected_condition]
        engagement = engagement[engagement['user_id'].isin(users['user_id'])]
        sessions = sessions[sessions['user_id'].isin(users['user_id'])]
        alerts = alerts[alerts['user_id'].isin(users['user_id'])]

st.subheader("Engagement Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Active Users", engagement.shape[0])
col2.metric("Avg Steps", int(engagement['avg_steps'].mean()))
col3.metric("Dropout Risk %", f"{round(engagement['dropout_risk'].mean()*100, 1)}%")

fig = px.histogram(engagement, x="avg_steps", nbins=30, title="Distribution of Average Daily Steps")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Session Outcomes")
sess_summary = sessions.groupby("session_type").agg({"outcome_score": "mean", "nps_score": "mean"}).reset_index()
fig2 = px.bar(sess_summary, x="session_type", y=["outcome_score", "nps_score"], barmode="group",
              title="Average Outcome & NPS Score by Session Type")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Alert Resolution")
alerts_summary = alerts.groupby("alert_type").agg({"resolved": ["count", "mean"]})
alerts_summary.columns = ["Total Alerts", "Resolution Rate"]
alerts_summary = alerts_summary.reset_index()
fig3 = px.bar(alerts_summary, x="alert_type", y="Resolution Rate", title="Alert Resolution Rate by Type")
st.plotly_chart(fig3, use_container_width=True)
