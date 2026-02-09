import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import os
from sklearn.metrics import confusion_matrix, roc_curve, auc, accuracy_score, precision_score, recall_score, f1_score

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Faculty Workload Intelligence System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM STYLING
# =========================
st.markdown("""
    <style>
        .metric-card {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
        .risk-high {
            background-color: #ffcccc;
            border-left: 4px solid #ff4b4b;
        }
        .risk-low {
            background-color: #ccffcc;
            border-left: 4px solid #09ab3b;
        }
    </style>
""", unsafe_allow_html=True)

# =========================
# LOAD MODEL & DATA
# =========================
model = joblib.load("models/logistic_regression_model.joblib")
scaler = joblib.load("models/scaler.joblib")

# Load training data for reference
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "faculty.db")

try:
    conn = sqlite3.connect(DB_PATH)
    train_data = pd.read_sql("SELECT * FROM faculty_workload", conn)
    conn.close()
    data_loaded = True
except:
    data_loaded = False
    train_data = None

# =========================
# HEADER
# =========================
st.markdown(
    """
    <h1 style='text-align: center; color: #1f77b4;'>📊 Faculty Workload Intelligence System</h1>
    <p style='text-align: center; font-size:16px; color: #666;'>
    Advanced Prediction • Comprehensive Analysis • Data-Driven Insights
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# =========================
# SIDEBAR
# =========================
st.sidebar.markdown("## 🎯 Navigation")
page = st.sidebar.radio(
    "Select Page:",
    ["📈 Single Prediction", "📊 Dataset Analysis", "🔬 Model Insights", "📋 About"]
)

# =========================
# PAGE 1: SINGLE PREDICTION
# =========================
if page == "📈 Single Prediction":
    st.subheader("🧑‍🏫 Faculty Workload Risk Predictor")
    
    st.write("""
    Enter faculty member details below to get a personalized workload risk assessment
    with detailed insights and recommendations.
    """)
    
    st.markdown("---")
    
    # Input section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Teaching Load")
        courses = st.selectbox("Courses Assigned", [1, 2, 3, 4])
        weekly_hours = st.slider("Weekly Teaching Hours", 5, 25, 12)
        students = st.slider("Total Students Handled", 30, 300, 120)
    
    with col2:
        st.markdown("### Administrative & Development")
        admin_roles = st.selectbox("Administrative Roles", [0, 1, 2])
        experience = st.slider("Years of Experience", 1, 30, 8)
        prep_hours = st.slider("Preparation Hours / Week", 5, 30, 12)
    
    with col3:
        st.markdown("### Academic Context")
        term = st.selectbox(
            "Academic Term",
            ["Independence Term", "Festival Term", "Republic Term", "Colors Term"]
        )
        exam = st.selectbox(
            "Exam Phase",
            ["Unit Test 1", "Mid Term", "Unit Test 2", "End Term"]
        )
    
    # Create input dataframe
    input_df = pd.DataFrame({
        "courses_assigned": [courses],
        "weekly_teaching_hours": [weekly_hours],
        "preparation_hours_per_week": [prep_hours],
        "total_students_handled": [students],
        "admin_roles_count": [admin_roles],
        "years_of_experience": [experience],
        "term": [term],
        "exam_type": [exam]
    })
    
    input_encoded = pd.get_dummies(
        input_df, columns=["term", "exam_type"], drop_first=True
    )
    input_encoded = input_encoded.reindex(
        columns=scaler.feature_names_in_, fill_value=0
    )
    
    input_scaled = scaler.transform(input_encoded)
    
    st.markdown("---")
    
    if st.button("🚀 Analyze Workload Risk", key="predict"):
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0][1]
        confidence = max(probability, 1 - probability)
        
        # Display prediction result
        col_result1, col_result2, col_result3 = st.columns(3)
        
        with col_result1:
            if prediction == 1:
                st.error("⚠️ HIGH RISK", icon="🔴")
            else:
                st.success("✅ LOW RISK", icon="🟢")
        
        with col_result2:
            st.metric("Risk Probability", f"{probability*100:.1f}%")
        
        with col_result3:
            st.metric("Confidence Score", f"{confidence*100:.1f}%")
        
        st.markdown("---")
        
        # Detailed Analysis
        st.subheader("📈 Detailed Workload Analysis")
        
        col_chart1, col_chart2 = st.columns(2)
        
        # Risk Probability Gauge
        with col_chart1:
            fig, ax = plt.subplots(figsize=(8, 4))
            categories = ['Low Risk', 'High Risk']
            values = [1 - probability, probability]
            colors = ['#09ab3b', '#ff4b4b']
            ax.pie(values, labels=categories, autopct='%1.1f%%', colors=colors, startangle=90)
            ax.set_title('Workload Risk Distribution', fontsize=14, fontweight='bold')
            st.pyplot(fig)
        
        # Workload Components
        with col_chart2:
            workload_components = pd.DataFrame({
                "Component": [
                    "Teaching",
                    "Preparation",
                    "Students",
                    "Admin"
                ],
                "Value": [
                    weekly_hours,
                    prep_hours,
                    students / 20,
                    admin_roles * 10
                ]
            })
            
            fig, ax = plt.subplots(figsize=(8, 4))
            bars = ax.barh(workload_components["Component"], workload_components["Value"], color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
            ax.set_xlabel('Contribution to Workload', fontsize=11)
            ax.set_title('Workload Component Breakdown', fontsize=14, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            st.pyplot(fig)
        
        st.markdown("---")
        
        # Detailed Metrics Table
        st.subheader("📊 Faculty Metrics Summary")
        
        metrics_summary = pd.DataFrame({
            "Metric": [
                "Courses Assigned",
                "Weekly Teaching Hours",
                "Total Students Handled",
                "Administrative Roles",
                "Years of Experience",
                "Preparation Hours/Week",
                "Academic Term",
                "Exam Phase"
            ],
            "Value": [
                f"{courses}",
                f"{weekly_hours} hrs",
                f"{students}",
                f"{admin_roles}",
                f"{experience} years",
                f"{prep_hours} hrs",
                term,
                exam
            ]
        })
        
        st.dataframe(metrics_summary, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Recommendations
        st.subheader("💡 Personalized Recommendations")
        
        recommendations = []
        
        if weekly_hours > 20:
            recommendations.append("🔴 **Reduce Teaching Load**: Your weekly teaching hours are high. Consider reducing course load or increasing prep time allocation.")
        
        if students > 150:
            recommendations.append("🟡 **Student Support**: With many students, implement efficient office hours and peer tutoring.")
        
        if admin_roles > 1:
            recommendations.append("🟡 **Administrative Burden**: Multiple admin roles detected. Delegate or streamline tasks where possible.")
        
        if experience < 3:
            recommendations.append("🔴 **Early Career Support**: As a newer faculty member, seek mentorship and professional development resources.")
        
        if exam in ["Mid Term", "End Term"] and weekly_hours > 15:
            recommendations.append("🔴 **Exam Period**: During major exam phases with high teaching load, plan ahead for grading time.")
        
        if prediction == 0 and len(recommendations) == 0:
            recommendations.append("🟢 **Well-Balanced**: Your workload appears well-distributed. Maintain current practices.")
        
        if recommendations:
            for rec in recommendations:
                st.write(rec)
        
        st.markdown("---")
        
        # Risk Score Explanation
        st.subheader("🧠 How the Prediction Works")
        st.info("""
        **Logistic Regression Model** analyzes multiple factors:
        - **Teaching Hours**: Direct instructional time and course responsibilities
        - **Preparation Work**: Time spent creating materials and grading
        - **Student Load**: Total number of students and mentoring requirements
        - **Administrative Tasks**: Committee work and leadership responsibilities
        - **Experience Level**: Seasoned faculty typically manage workload better
        - **Academic Context**: Different terms and exam phases have varying demands
        
        The model combines these factors to calculate a probability score between 0% and 100%.
        """)

# =========================
# PAGE 2: DATASET ANALYSIS
# =========================
elif page == "📊 Dataset Analysis":
    st.subheader("📊 Faculty Workload Dataset Overview")
    
    if data_loaded and train_data is not None:
        st.write(f"Total Faculty Members in Dataset: **{len(train_data)}**")
        
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        with col_stat1:
            high_risk = len(train_data[train_data['workload_risk'] == 1])
            st.metric("High Risk Faculty", high_risk, f"{high_risk/len(train_data)*100:.1f}%")
        
        with col_stat2:
            low_risk = len(train_data[train_data['workload_risk'] == 0])
            st.metric("Low Risk Faculty", low_risk, f"{low_risk/len(train_data)*100:.1f}%")
        
        with col_stat3:
            avg_courses = train_data['courses_assigned'].mean()
            st.metric("Avg Courses Assigned", f"{avg_courses:.1f}")
        
        with col_stat4:
            avg_students = train_data['total_students_handled'].mean()
            st.metric("Avg Students Handled", f"{int(avg_students)}")
        
        st.markdown("---")
        
        # Visualizations
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            fig, ax = plt.subplots(figsize=(8, 5))
            risk_counts = train_data['workload_risk'].value_counts()
            colors = ['#09ab3b', '#ff4b4b']
            ax.bar(['Low Risk', 'High Risk'], [risk_counts[0], risk_counts[1]], color=colors)
            ax.set_ylabel('Number of Faculty', fontsize=11)
            ax.set_title('Risk Distribution in Dataset', fontsize=13, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            for i, v in enumerate([risk_counts[0], risk_counts[1]]):
                ax.text(i, v + 1, str(v), ha='center', fontweight='bold')
            st.pyplot(fig)
        
        with col_viz2:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.scatter(train_data[train_data['workload_risk']==0]['weekly_teaching_hours'],
                      train_data[train_data['workload_risk']==0]['total_students_handled'],
                      color='#09ab3b', label='Low Risk', s=80, alpha=0.6)
            ax.scatter(train_data[train_data['workload_risk']==1]['weekly_teaching_hours'],
                      train_data[train_data['workload_risk']==1]['total_students_handled'],
                      color='#ff4b4b', label='High Risk', s=80, alpha=0.6)
            ax.set_xlabel('Weekly Teaching Hours', fontsize=11)
            ax.set_ylabel('Total Students Handled', fontsize=11)
            ax.set_title('Teaching Load vs Student Load', fontsize=13, fontweight='bold')
            ax.legend()
            ax.grid(alpha=0.3)
            st.pyplot(fig)
        
        st.markdown("---")
        
        col_viz3, col_viz4 = st.columns(2)
        
        with col_viz3:
            fig, ax = plt.subplots(figsize=(8, 5))
            term_risk = pd.crosstab(train_data['term'], train_data['workload_risk'])
            term_risk.plot(kind='bar', ax=ax, color=['#09ab3b', '#ff4b4b'])
            ax.set_xlabel('Academic Term', fontsize=11)
            ax.set_ylabel('Number of Faculty', fontsize=11)
            ax.set_title('Risk by Academic Term', fontsize=13, fontweight='bold')
            ax.legend(['Low Risk', 'High Risk'])
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)
        
        with col_viz4:
            fig, ax = plt.subplots(figsize=(8, 5))
            exam_risk = pd.crosstab(train_data['exam_type'], train_data['workload_risk'])
            exam_risk.plot(kind='bar', ax=ax, color=['#09ab3b', '#ff4b4b'])
            ax.set_xlabel('Exam Type', fontsize=11)
            ax.set_ylabel('Number of Faculty', fontsize=11)
            ax.set_title('Risk by Exam Type', fontsize=13, fontweight='bold')
            ax.legend(['Low Risk', 'High Risk'])
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)
        
        st.markdown("---")
        
        # Summary Statistics
        st.subheader("📈 Summary Statistics")
        st.dataframe(train_data.describe(), use_container_width=True)
    else:
        st.warning("⚠️ Dataset not loaded. Please ensure the database file exists.")

# =========================
# PAGE 3: MODEL INSIGHTS
# =========================
elif page == "🔬 Model Insights":
    st.subheader("🔬 Machine Learning Model Analysis")
    
    st.write("""
    This section provides insights into how the Logistic Regression model works
    and its performance characteristics.
    """)
    
    st.markdown("---")
    
    # Model Information
    st.subheader("📋 Model Information")
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown("""
        **Model Type:** Logistic Regression  
        **Algorithm:** Binary Classification  
        **Framework:** Scikit-Learn  
        **Purpose:** Predict workload risk (0 = Low, 1 = High)
        """)
    
    with col_info2:
        st.markdown("""
        **Features Used:** 8 (after encoding)  
        **Training Samples:** 120  
        **Test Size:** 25%  
        **Random State:** 42
        """)
    
    st.markdown("---")
    
    # Features and Their Importance
    st.subheader("🎯 Model Features")
    
    features_info = pd.DataFrame({
        "Feature": [
            "Courses Assigned",
            "Weekly Teaching Hours",
            "Preparation Hours/Week",
            "Total Students Handled",
            "Admin Roles Count",
            "Years of Experience",
            "Term (Encoded)",
            "Exam Type (Encoded)"
        ],
        "Type": [
            "Numeric",
            "Numeric",
            "Numeric",
            "Numeric",
            "Numeric",
            "Numeric",
            "Categorical",
            "Categorical"
        ],
        "Impact on Risk": [
            "Higher → More Risk",
            "Higher → More Risk",
            "Higher → More Risk",
            "Higher → More Risk",
            "Higher → More Risk",
            "Higher → Less Risk",
            "Context-dependent",
            "Context-dependent"
        ]
    })
    
    st.dataframe(features_info, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Model Coefficients Visualization
    st.subheader("📊 Feature Coefficients")
    
    coefficients = model.coef_[0]
    feature_names = scaler.feature_names_in_
    
    coef_df = pd.DataFrame({
        "Feature": feature_names,
        "Coefficient": coefficients
    }).sort_values("Coefficient")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#ff4b4b' if x > 0 else '#09ab3b' for x in coef_df['Coefficient']]
    ax.barh(coef_df["Feature"], coef_df["Coefficient"], color=colors)
    ax.set_xlabel('Coefficient Value', fontsize=11)
    ax.set_title('Feature Impact on High Risk Prediction', fontsize=13, fontweight='bold')
    ax.axvline(x=0, color='black', linestyle='--', linewidth=0.8)
    ax.grid(axis='x', alpha=0.3)
    st.pyplot(fig)
    
    st.info("""
    **Interpretation:**
    - 🔴 **Red bars (positive)**: Increase the likelihood of HIGH RISK prediction
    - 🟢 **Green bars (negative)**: Increase the likelihood of LOW RISK prediction
    """)
    
    st.markdown("---")
    
    # Model Performance Metrics
    st.subheader("⚙️ Model Configuration & Metrics")
    
    col_perf1, col_perf2, col_perf3 = st.columns(3)
    
    with col_perf1:
        st.markdown("""
        **Intercept (Bias):** {:.4f}
        
        **Regularization:** L2 (Ridge)  
        **Max Iterations:** 1000  
        **Solver:** lbfgs
        """.format(model.intercept_[0]))
    
    with col_perf2:
        st.markdown("""
        **Scaling Method:** StandardScaler
        
        **Mean Normalization:** Applied  
        **Standard Deviation:** Applied  
        **Fit on:** Training data (90 samples)
        """)
    
    with col_perf3:
        st.markdown("""
        **Prediction Threshold:** 0.5
        
        **Probability Output:** [0, 1]  
        **Decision Rule:** P(High Risk) ≥ 0.5
        """)

# =========================
# PAGE 4: ABOUT
# =========================
elif page == "📋 About":
    st.subheader("📋 About this System")
    
    st.markdown("""
    ## Faculty Workload Intelligence System
    
    ### 🎯 Purpose
    This system helps academic institutions assess faculty workload risk and provide
    data-driven insights for resource allocation and workload distribution planning.
    
    ### 📊 Data Sources
    - **Training Data**: 120 faculty records with synthetic but realistic attributes
    - **Features**: 8 key factors including teaching load, admin roles, and experience
    - **Target**: Binary classification (High Risk / Low Risk workload)
    
    ### 🤖 Technology Stack
    - **Frontend**: Streamlit
    - **ML Framework**: Scikit-Learn (Logistic Regression)
    - **Data Processing**: Pandas, NumPy
    - **Visualization**: Matplotlib, Seaborn
    - **Database**: SQLite
    
    ### 📈 Key Features
    1. **Single Prediction**: Get personalized workload risk assessment
    2. **Dataset Analysis**: Explore patterns in faculty workload distribution
    3. **Model Insights**: Understand how the ML model makes decisions
    4. **Recommendations**: Get actionable insights for workload management
    
    ### 🔬 Model Details
    - **Type**: Logistic Regression (Binary Classification)
    - **Training Samples**: 120 faculty records
    - **Test Size**: 25% of data
    - **Features**: 8 (numeric + encoded categorical)
    - **Regularization**: L2 (Ridge) with C=1.0
    
    ### 💡 How to Use
    1. Go to **"📈 Single Prediction"** tab to predict risk for a faculty member
    2. Go to **"📊 Dataset Analysis"** to see patterns in the training data
    3. Go to **"🔬 Model Insights"** to understand model behavior
    4. Refer to recommendations generated for each prediction
    
    ### ⚠️ Important Notes
    - Predictions are based on patterns from synthetic training data
    - Real-world validation with actual data is recommended
    - Use predictions as a decision support, not absolute decision making tools
    - Consider qualitative factors alongside quantitative predictions
    
    ### 👥 Contact & Support
    For questions or improvements, please reach out to the development team.
    
    ---
    
    **Version**: 1.0  
    **Last Updated**: February 2026  
    **Status**: Production Ready ✅
    """)

st.markdown("---")
st.caption("Faculty Workload Intelligence System © 2026 • Hackathon 3 Project")