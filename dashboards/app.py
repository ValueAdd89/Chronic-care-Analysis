import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import numpy as np # For numerical operations and NaN handling

# --- Page Configuration ---
st.set_page_config(
    layout="wide",
    page_title="ChronicCare Analytics Dashboard",
    page_icon="📊"
)

st.title("📊 ChronicCare Analytics Dashboard")
st.markdown("---")

# --- Data Loading (Cached for performance) ---
@st.cache_data
def load_data():
    base_path = Path("data") # Assumes data folder is sibling to app.py, adjust if app.py is in a subfolder

    try:
        users = pd.read_csv(base_path / "users.csv")
        engagement = pd.read_csv(base_path / "ml_engagement_training_data.csv")
        sessions = pd.read_csv(base_path / "clinical_sessions.csv")
        alerts = pd.read_csv(base_path / "ai_alerts.csv")

        # --- Initial Data Cleaning/Preparation ---
        # Ensure user_id is consistent for merging if needed across files
        # Convert date columns to datetime objects
        if 'session_date' in sessions.columns:
            sessions['session_date'] = pd.to_datetime(sessions['session_date'], errors='coerce')
        if 'alert_date' in alerts.columns:
            alerts['alert_date'] = pd.to_datetime(alerts['alert_date'], errors='coerce')
        if 'date' in engagement.columns: # Assuming engagement might have a date column
            engagement['date'] = pd.to_datetime(engagement['date'], errors='coerce')

        # Drop rows with NaT (Not a Time) values if conversion failed
        sessions.dropna(subset=['session_date'], inplace=True)
        alerts.dropna(subset=['alert_date'], inplace=True)
        
        return users, engagement, sessions, alerts
    except FileNotFoundError as e:
        st.error(f"Required data file not found: {e.filename}. Please ensure all CSVs are in the 'data/' directory.")
        st.stop()
    except Exception as e:
        st.error(f"An error occurred during data loading: {e}. Please check your CSV file contents.")
        st.stop()

users_orig, engagement_orig, sessions_orig, alerts_orig = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Filter Dashboard Data")

# Condition Filter
condition_options = ["All"] + sorted(users_orig['condition'].unique().tolist())
selected_condition = st.sidebar.selectbox("Condition", options=condition_options)

# Gender Filter (assuming 'gender' column exists in users.csv)
if 'gender' in users_orig.columns:
    gender_options = ["All"] + sorted(users_orig['gender'].unique().tolist())
    selected_gender = st.sidebar.selectbox("Gender", options=gender_options)
else:
    selected_gender = "All"
    st.sidebar.info("Gender filter not available (column missing).")

# Alert Type Filter (assuming 'alert_type' column exists in ai_alerts.csv)
if 'alert_type' in alerts_orig.columns:
    alert_type_options = ["All"] + sorted(alerts_orig['alert_type'].unique().tolist())
    selected_alert_type = st.sidebar.selectbox("Alert Type", options=alert_type_options)
else:
    selected_alert_type = "All"
    st.sidebar.info("Alert Type filter not available (column missing).")

# Date Range Filter (for sessions and alerts)
min_date_val = min(sessions_orig['session_date'].min(), alerts_orig['alert_date'].min())
max_date_val = max(sessions_orig['session_date'].max(), alerts_orig['alert_date'].max())

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date_val, max_date_val),
    min_value=min_date_val,
    max_value=max_date_val
)

# Ensure date_range has two elements, especially during initial load
if len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1]) + pd.Timedelta(days=1) # Include the end date
else:
    start_date = pd.to_datetime(min_date_val)
    end_date = pd.to_datetime(max_date_val) + pd.Timedelta(days=1)


# --- Apply Global Filters ---
# Start with copies of original dataframes to avoid modifying cached data
filtered_users = users_orig.copy()
filtered_engagement = engagement_orig.copy()
filtered_sessions = sessions_orig.copy()
filtered_alerts = alerts_orig.copy()

# Filter users based on condition and gender
if selected_condition != "All":
    filtered_users = filtered_users[filtered_users['condition'] == selected_condition]
if selected_gender != "All" and 'gender' in filtered_users.columns:
    filtered_users = filtered_users[filtered_users['gender'] == selected_gender]

# Filter other dataframes based on user_ids present in filtered_users
user_ids_in_filter = filtered_users['user_id'].unique()
filtered_engagement = filtered_engagement[filtered_engagement['user_id'].isin(user_ids_in_filter)]
filtered_sessions = filtered_sessions[filtered_sessions['user_id'].isin(user_ids_in_filter)]
filtered_alerts = filtered_alerts[filtered_alerts['user_id'].isin(user_ids_in_filter)]

# Apply date range filter to sessions and alerts
filtered_sessions = filtered_sessions[
    (filtered_sessions['session_date'] >= start_date) &
    (filtered_sessions['session_date'] < end_date)
]
filtered_alerts = filtered_alerts[
    (filtered_alerts['alert_date'] >= start_date) &
    (filtered_alerts['alert_date'] < end_date)
]

# Apply Alert Type filter
if selected_alert_type != "All" and 'alert_type' in filtered_alerts.columns:
    filtered_alerts = filtered_alerts[filtered_alerts['alert_type'] == selected_alert_type]


# --- Check if data remains after filtering ---
if filtered_users.empty:
    st.warning("No data available for the selected filters. Please adjust your selections.")
    st.stop() # Stop execution if no data

# --- Dashboard Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard Overview",
    "👥 User Engagement",
    "🩺 Clinical Sessions",
    "🚨 AI Alerts"
])

# --- Tab 1: Dashboard Overview ---
with tab1:
    st.header("Overall Performance & Key Metrics")

    # KPIs
    total_users_kpi = filtered_users.shape[0]
    total_active_users_kpi = filtered_engagement['user_id'].nunique()
    total_sessions_kpi = filtered_sessions.shape[0]
    total_alerts_kpi = filtered_alerts.shape[0]

    avg_steps_kpi = filtered_engagement['avg_steps'].mean() if not filtered_engagement.empty and 'avg_steps' in filtered_engagement.columns else 0
    avg_outcome_score_kpi = filtered_sessions['outcome_score'].mean() if not filtered_sessions.empty and 'outcome_score' in filtered_sessions.columns else 0
    avg_nps_score_kpi = filtered_sessions['nps_score'].mean() if not filtered_sessions.empty and 'nps_score' in filtered_sessions.columns else 0
    
    # Calculate overall alert resolution rate
    total_resolved_alerts = filtered_alerts['resolved'].sum() if 'resolved' in filtered_alerts.columns else 0
    alert_resolution_rate_kpi = (total_resolved_alerts / total_alerts_kpi * 100) if total_alerts_kpi > 0 else 0

    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    col_kpi1.metric("Total Users", f"{total_users_kpi:,}")
    col_kpi2.metric("Active Users (in Engagement)", f"{total_active_users_kpi:,}")
    col_kpi3.metric("Avg Daily Steps", f"{int(avg_steps_kpi):,}")
    col_kpi4.metric("Avg Session Outcome Score", f"{avg_outcome_score_kpi:.1f}")

    col_kpi5, col_kpi6, col_kpi7, col_kpi8 = st.columns(4)
    col_kpi5.metric("Avg Session NPS Score", f"{avg_nps_score_kpi:.1f}")
    col_kpi6.metric("Total Clinical Sessions", f"{total_sessions_kpi:,}")
    col_kpi7.metric("Total AI Alerts", f"{total_alerts_kpi:,}")
    col_kpi8.metric("Alert Resolution Rate", f"{alert_resolution_rate_kpi:.1f}%")

    st.markdown("---")
    st.subheader("User Distribution by Condition & Gender")

    col_dist1, col_dist2 = st.columns(2)

    with col_dist1:
        if 'condition' in filtered_users.columns and not filtered_users['condition'].empty:
            condition_counts = filtered_users['condition'].value_counts().reset_index()
            condition_counts.columns = ['Condition', 'Count']
            fig_condition = px.bar(condition_counts, x='Condition', y='Count', title='Users by Condition', text='Count')
            fig_condition.update_traces(texttemplate='%{text}', textposition='outside')
            st.plotly_chart(fig_condition, use_container_width=True)
        else:
            st.info("No condition data available for distribution.")

    with col_dist2:
        if 'gender' in filtered_users.columns and not filtered_users['gender'].empty:
            gender_counts = filtered_users['gender'].value_counts().reset_index()
            gender_counts.columns = ['Gender', 'Count']
            fig_gender = px.pie(gender_counts, values='Count', names='Gender', title='Users by Gender', hole=0.3)
            st.plotly_chart(fig_gender, use_container_width=True)
        else:
            st.info("No gender data available for distribution.")

# --- Tab 2: User Engagement ---
with tab2:
    st.header("User Engagement & Risk Profile")

    col_engage1, col_engage2 = st.columns(2)

    with col_engage1:
        st.subheader("Distribution of Average Daily Steps")
        if not filtered_engagement.empty and 'avg_steps' in filtered_engagement.columns:
            fig_steps_hist = px.histogram(filtered_engagement, x="avg_steps", nbins=30, title="Distribution of Average Daily Steps")
            st.plotly_chart(fig_steps_hist, use_container_width=True)
        else:
            st.info("No engagement data (avg_steps) available for this view.")

    with col_engage2:
        st.subheader("Dropout Risk Distribution")
        if not filtered_engagement.empty and 'dropout_risk' in filtered_engagement.columns:
            # Categorize dropout risk for better visualization
            bins = [0, 0.25, 0.5, 0.75, 1.0]
            labels = ['Low Risk', 'Moderate Risk', 'High Risk', 'Very High Risk']
            filtered_engagement['risk_category'] = pd.cut(filtered_engagement['dropout_risk'], bins=bins, labels=labels, right=False)
            
            risk_counts = filtered_engagement['risk_category'].value_counts().reset_index()
            risk_counts.columns = ['Risk Category', 'Count']
            risk_counts['Risk Category'] = pd.Categorical(risk_counts['Risk Category'], categories=labels, ordered=True) # Ensure order
            risk_counts = risk_counts.sort_values('Risk Category')

            fig_risk_pie = px.pie(risk_counts, values='Count', names='Risk Category', title='Dropout Risk Distribution', hole=0.4,
                                  color_discrete_map={'Low Risk':'#2ecc71', 'Moderate Risk':'#f1c40f', 'High Risk':'#e67e22', 'Very High Risk':'#e74c3c'})
            st.plotly_chart(fig_risk_pie, use_container_width=True)
        else:
            st.info("No engagement data (dropout_risk) available for this view.")

    st.markdown("---")
    st.subheader("Engagement Metrics by User Condition")
    if not filtered_engagement.empty and 'user_id' in filtered_engagement.columns and 'condition' in filtered_users.columns:
        # Merge engagement with user conditions for this analysis
        engagement_with_condition = pd.merge(filtered_engagement, filtered_users[['user_id', 'condition']], on='user_id', how='left')
        
        if not engagement_with_condition.empty and 'avg_steps' in engagement_with_condition.columns and 'dropout_risk' in engagement_with_condition.columns:
            avg_metrics_by_condition = engagement_with_condition.groupby('condition').agg(
                avg_steps=('avg_steps', 'mean'),
                avg_dropout_risk=('dropout_risk', 'mean'),
                user_count=('user_id', 'nunique')
            ).reset_index()

            col_cond_engage1, col_cond_engage2 = st.columns(2)
            with col_cond_engage1:
                fig_steps_by_cond = px.bar(avg_metrics_by_condition, x='condition', y='avg_steps', title='Avg Daily Steps by Condition', text='avg_steps')
                fig_steps_by_cond.update_traces(texttemplate='%{text:.0f}', textposition='outside')
                st.plotly_chart(fig_steps_by_cond, use_container_width=True)
            with col_cond_engage2:
                fig_risk_by_cond = px.bar(avg_metrics_by_condition, x='condition', y='avg_dropout_risk', title='Avg Dropout Risk by Condition', text='avg_dropout_risk')
                fig_risk_by_cond.update_traces(texttemplate='%{text:.2f}', textposition='outside')
                st.plotly_chart(fig_risk_by_cond, use_container_width=True)
        else:
            st.info("Engagement metrics by condition not available for display.")
    else:
        st.info("User or engagement data insufficient for engagement by condition analysis.")

# --- Tab 3: Clinical Sessions ---
with tab3:
    st.header("Clinical Sessions Outcomes & Trends")

    st.subheader("Average Outcome & NPS Score by Session Type")
    if not filtered_sessions.empty and 'session_type' in filtered_sessions.columns:
        sess_summary = filtered_sessions.groupby("session_type").agg({
            "outcome_score": "mean",
            "nps_score": "mean",
            "user_id": "nunique" # Count users per session type
        }).reset_index()
        sess_summary.columns = ["session_type", "Average Outcome Score", "Average NPS Score", "Unique Users"]
        
        col_sess_summ1, col_sess_summ2 = st.columns(2)
        with col_sess_summ1:
            fig2 = px.bar(sess_summary, x="session_type", y=["Average Outcome Score", "Average NPS Score"], barmode="group",
                            title="Average Outcome & NPS Score by Session Type")
            st.plotly_chart(fig2, use_container_width=True)
        with col_sess_summ2:
            fig_sess_users = px.bar(sess_summary, x="session_type", y="Unique Users", title="Unique Users by Session Type", text="Unique Users")
            fig_sess_users.update_traces(texttemplate='%{text}', textposition='outside')
            st.plotly_chart(fig_sess_users, use_container_width=True)
    else:
        st.info("No session data available for outcome and NPS analysis.")
    
    st.markdown("---")
    st.subheader("Sessions Over Time")
    if not filtered_sessions.empty and 'session_date' in filtered_sessions.columns:
        sessions_daily = filtered_sessions.groupby(pd.Grouper(key='session_date', freq='D')).size().reset_index(name='Count')
        fig_sessions_trend = px.line(sessions_daily, x='session_date', y='Count', title='Daily Clinical Sessions Trend')
        st.plotly_chart(fig_sessions_trend, use_container_width=True)
    else:
        st.info("No session data or date information for trend analysis.")

# --- Tab 4: AI Alerts ---
with tab4:
    st.header("AI Alerts Analysis & Resolution")

    st.subheader("Alert Resolution Rate by Type")
    if not filtered_alerts.empty and 'alert_type' in filtered_alerts.columns:
        alerts_summary = filtered_alerts.groupby("alert_type").agg(
            total_alerts=("user_id", "count"), # Count total alerts
            resolved_alerts=("resolved", "sum") # Sum of resolved (assuming 'resolved' is 0/1)
        ).reset_index()
        alerts_summary['resolution_rate'] = (alerts_summary['resolved_alerts'] / alerts_summary['total_alerts'] * 100)
        
        col_alert1, col_alert2 = st.columns(2)
        with col_alert1:
            fig3 = px.bar(alerts_summary, x="alert_type", y="resolution_rate", title="Alert Resolution Rate by Type", text="resolution_rate")
            fig3.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            st.plotly_chart(fig3, use_container_width=True)
        
        with col_alert2:
            # Overall Resolved vs Unresolved
            overall_resolved_count = alerts_summary['resolved_alerts'].sum()
            overall_total_alerts = alerts_summary['total_alerts'].sum()
            overall_unresolved_count = overall_total_alerts - overall_resolved_count

            overall_resolution_data = pd.DataFrame({
                'Status': ['Resolved', 'Unresolved'],
                'Count': [overall_resolved_count, overall_unresolved_count]
            })
            fig_overall_res = px.pie(overall_resolution_data, values='Count', names='Status', title='Overall Alert Resolution Status', hole=0.4,
                                     color_discrete_map={'Resolved':'#2ecc71', 'Unresolved':'#e74c3c'})
            st.plotly_chart(fig_overall_res, use_container_width=True)
    else:
        st.info("No alert data available for resolution analysis.")

    st.markdown("---")
    st.subheader("Alerts Over Time")
    if not filtered_alerts.empty and 'alert_date' in filtered_alerts.columns:
        alerts_daily = filtered_alerts.groupby(pd.Grouper(key='alert_date', freq='D')).size().reset_index(name='Count')
        fig_alerts_trend = px.line(alerts_daily, x='alert_date', y='Count', title='Daily AI Alerts Trend')
        st.plotly_chart(fig_alerts_trend, use_container_width=True)
    else:
        st.info("No alert data or date information for trend analysis.")

    st.markdown("---")
    st.subheader("Alerts by User Condition")
    if not filtered_alerts.empty and 'user_id' in filtered_alerts.columns and 'condition' in filtered_users.columns:
        alerts_with_condition = pd.merge(filtered_alerts, filtered_users[['user_id', 'condition']], on='user_id', how='left')
        
        if not alerts_with_condition.empty and 'condition' in alerts_with_condition.columns:
            alert_counts_by_condition = alerts_with_condition.groupby('condition')['user_id'].count().reset_index()
            alert_counts_by_condition.columns = ['Condition', 'Total Alerts']
            
            fig_alerts_by_cond = px.bar(alert_counts_by_condition, x='Condition', y='Total Alerts', title='Total Alerts by User Condition', text='Total Alerts')
            fig_alerts_by_cond.update_traces(texttemplate='%{text}', textposition='outside')
            st.plotly_chart(fig_alerts_by_cond, use_container_width=True)
        else:
            st.info("Alerts by user condition not available for display.")
    else:
        st.info("User or alert data insufficient for alerts by condition analysis.")
