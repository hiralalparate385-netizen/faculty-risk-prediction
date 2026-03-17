import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
from pathlib import Path
from streamlit_option_menu import option_menu

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(
    page_title="Faculty Workload AI",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
DATABASE_PATH = BASE_DIR / "data" / "faculty.db"
MODEL_PATH = BASE_DIR / "models" / "logistic_model.joblib"
SCALER_PATH = BASE_DIR / "models" / "logistic_scaler.joblib"

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    conn = sqlite3.connect(DATABASE_PATH)
    df = pd.read_sql_query("SELECT * FROM faculty_workload_cleaned", conn)
    conn.close()
    return df

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH), joblib.load(SCALER_PATH)

df = load_data()
model, scaler = load_model()

# -------------------------------
# SIDEBAR MENU
# -------------------------------
with st.sidebar:
    selected = option_menu(
        "Dashboard",
        ["Overview", "EDA", "Prediction"],
        icons=["house", "bar-chart", "robot"],
        menu_icon="cast",
        default_index=0,
    )

# -------------------------------
# OVERVIEW
# -------------------------------
if selected == "Overview":
    st.title("📊 Faculty Workload Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Faculty", len(df))
    col2.metric("High Risk", int(df['workload_risk'].sum()))
    col3.metric("Low Risk", int((df['workload_risk'] == 0).sum()))

    st.markdown("---")

    # Pie chart
    fig = px.pie(
        df,
        names='workload_risk',
        title="Workload Risk Distribution",
        color_discrete_sequence=['green', 'red']
    )
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# EDA
# -------------------------------
elif selected == "EDA":
    st.title("📊 Exploratory Data Analysis")

    col1, col2 = st.columns(2)

    # Histogram
    feature = st.selectbox("Select Feature", [
        'courses_assigned',
        'weekly_teaching_hours',
        'total_students_handled',
        'admin_roles_count',
        'years_of_experience',
        'preparation_hours_per_week'
    ])

    fig = px.histogram(df, x=feature, color="workload_risk", barmode="overlay")
    st.plotly_chart(fig, use_container_width=True)

    # Boxplot
    fig2 = px.box(df, x="workload_risk", y=feature)
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # Correlation heatmap
    corr = df.corr(numeric_only=True)
    fig3 = px.imshow(corr, text_auto=True, aspect="auto")
    st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# PREDICTION
# -------------------------------
elif selected == "Prediction":
    st.title("🤖 Predict Faculty Workload Risk")

    st.markdown("### Enter Faculty Details")

    col1, col2 = st.columns(2)

    with col1:
        courses = st.slider("Courses Assigned", 1, 6, 3)
        weekly_hours = st.slider("Weekly Hours", 0, 30, 12)
        students = st.slider("Students", 10, 300, 100)

    with col2:
        admin_roles = st.slider("Admin Roles", 0, 5, 1)
        experience = st.slider("Experience (Years)", 1, 40, 10)
        prep_hours = st.slider("Preparation Hours", 0, 20, 5)

    # Dummy encoded placeholders
    term_cols = [0,0,0,0]
    exam_cols = [0,0,0,0]

    input_data = np.array([[
        courses,
        weekly_hours,
        students,
        admin_roles,
        experience,
        prep_hours,
        *term_cols,
        *exam_cols
    ]])

    input_scaled = scaler.transform(input_data)

    st.markdown("---")

    if st.button("🔍 Predict Risk", use_container_width=True):
        prob = model.predict_proba(input_scaled)[0][1]
        prediction = model.predict(input_scaled)[0]

        if prediction == 1:
            st.error("⚠️ HIGH RISK")
        else:
            st.success("✅ LOW RISK")

        # Gauge chart
        fig = px.bar(
            x=["Risk Probability"],
            y=[prob],
            range_y=[0,1],
            title="Risk Score"
        )
        st.plotly_chart(fig, use_container_width=True)