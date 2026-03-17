import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from streamlit_option_menu import option_menu
import json

# ======================== PAGE CONFIG ========================
st.set_page_config(
    page_title="Faculty Workload Prediction System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================== CUSTOM CSS ========================
st.markdown("""
    <style>
    :root {
        --primary-color: #FF6B6B;
        --secondary-color: #4ECDC4;
        --dark-bg: #0F1419;
        --light-bg: #1A1F2E;
        --accent: #FFD93D;
        --text-light: #E8E8E8;
    }
    
    * {
        margin: 0;
        padding: 0;
    }
    
    .main {
        background: linear-gradient(135deg, #0F1419 0%, #1A1F2E 100%);
        color: #E8E8E8;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        color: #E8E8E8;
        background-color: transparent;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: rgba(255, 107, 107, 0.2);
        color: #FF6B6B;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1A1F2E 0%, #252D3D 100%);
        border-left: 4px solid #FF6B6B;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .header-title {
        font-size: 2.5em;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .subtitle {
        font-size: 1.1em;
        color: #A0A0A0;
        margin-bottom: 20px;
    }
    
    .risk-high {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.2) 0%, rgba(255, 107, 107, 0.1) 100%);
        border-left: 4px solid #FF6B6B;
        color: #FF6B6B;
        padding: 15px;
        border-radius: 8px;
    }
    
    .risk-low {
        background: linear-gradient(135deg, rgba(78, 205, 196, 0.2) 0%, rgba(78, 205, 196, 0.1) 100%);
        border-left: 4px solid #4ECDC4;
        color: #4ECDC4;
        padding: 15px;
        border-radius: 8px;
    }
    
    .insight-box {
        background: rgba(255, 217, 61, 0.1);
        border-left: 4px solid #FFD93D;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        color: #E8E8E8;
    }
    
    .chart-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 15px;
        margin: 15px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ======================== PATHS & DATA LOADING ========================
BASE_DIR = Path(__file__).parent
DATABASE_PATH = BASE_DIR / "data" / "faculty.db"
MODEL_PATH = BASE_DIR / "models" / "logistic_model.joblib"
SCALER_PATH = BASE_DIR / "models" / "logistic_scaler.joblib"
MODELS_DIR = BASE_DIR / "models"

@st.cache_data
def load_data():
    conn = sqlite3.connect(DATABASE_PATH)
    df = pd.read_sql_query("SELECT * FROM faculty_workload_cleaned", conn)
    conn.close()
    return df

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH), joblib.load(SCALER_PATH)

@st.cache_data
def load_all_models_metadata():
    metadata = {}
    for model_file in MODELS_DIR.glob("*_metadata.json"):
        with open(model_file) as f:
            metadata[model_file.stem.replace("_metadata", "")] = json.load(f)
    return metadata

df = load_data()
model, scaler = load_model()
models_metadata = load_all_models_metadata()

# ======================== SIDEBAR MENU ========================
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; margin: 20px 0;'>
            <h1 style='color: #FF6B6B; font-size: 2em;'>🎓</h1>
            <h2 style='color: #E8E8E8; font-weight: 800;'>FacultyAI</h2>
            <p style='color: #A0A0A0; font-size: 0.9em;'>Workload Risk Prediction</p>
        </div>
        <hr style='border-color: rgba(255, 255, 255, 0.1);'>
    """, unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["🏠 Dashboard", "📊 Analytics", "🔮 Prediction", "📈 Model Comparison", "ℹ️ About"],
        icons=["house", "bar-chart", "robot", "graph-up", "info-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#FF6B6B", "font-size": "18px"},
            "nav-link": {"color": "#E8E8E8", "font-size": "16px", "text-align": "left", "margin": "10px 0", "--hover-color": "rgba(255, 107, 107, 0.2)"},
            "nav-link-selected": {"background-color": "rgba(255, 107, 107, 0.3)", "color": "#FF6B6B", "font-weight": "700"},
        }
    )
    
    st.sidebar.markdown("""
        <hr style='border-color: rgba(255, 255, 255, 0.1); margin: 30px 0;'>
        <p style='text-align: center; color: #A0A0A0; font-size: 0.85em;'>
            <strong>Dataset Stats:</strong><br>
            Total Faculty: """ + str(len(df)) + """<br>
            High Risk: """ + str(int(df['workload_risk'].sum())) + """<br>
            Low Risk: """ + str(int((df['workload_risk'] == 0).sum())) + """
        </p>
    """, unsafe_allow_html=True)

# ======================== MAIN HEADER ========================
st.markdown("""
    <div style='text-align: center; margin: 30px 0 40px 0;'>
        <h1 class='header-title'>🎓 Faculty Workload Risk Prediction</h1>
        <p class='subtitle'>AI-Powered System for Identifying Faculty Overload Risk</p>
    </div>
""", unsafe_allow_html=True)

# ======================== DASHBOARD ========================
if selected == "🏠 Dashboard":
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class='metric-card'>
                <div style='font-size: 2.5em;'>👥</div>
                <div style='font-size: 0.9em; color: #A0A0A0;'>Total Faculty</div>
                <div style='font-size: 2em; font-weight: 800; color: #FF6B6B;'>""" + str(len(df)) + """</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        high_risk = int(df['workload_risk'].sum())
        st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 2.5em;'>⚠️</div>
                <div style='font-size: 0.9em; color: #A0A0A0;'>High Risk</div>
                <div style='font-size: 2em; font-weight: 800; color: #FF6B6B;'>{high_risk}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        low_risk = int((df['workload_risk'] == 0).sum())
        st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 2.5em;'>✅</div>
                <div style='font-size: 0.9em; color: #A0A0A0;'>Low Risk</div>
                <div style='font-size: 2em; font-weight: 800; color: #4ECDC4;'>{low_risk}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        risk_percentage = round((high_risk / len(df)) * 100, 1)
        st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 2.5em;'>📊</div>
                <div style='font-size: 0.9em; color: #A0A0A0;'>Risk Rate</div>
                <div style='font-size: 2em; font-weight: 800; color: #FFD93D;'>{risk_percentage}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("📊 Risk Distribution")
        fig_pie = px.pie(
            values=[low_risk, high_risk],
            names=['Low Risk', 'High Risk'],
            color_discrete_sequence=['#4ECDC4', '#FF6B6B'],
            hole=0.3
        )
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E8E8E8'),
            height=400
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("📈 Risk by Experience Level")
        experience_risk = df.groupby(pd.cut(df['years_of_experience'], bins=5))['workload_risk'].mean()
        fig_exp = px.bar(
            x=[f"{int(x.left)}-{int(x.right)}" for x in experience_risk.index],
            y=experience_risk.values,
            color=experience_risk.values,
            color_continuous_scale=['#4ECDC4', '#FFD93D', '#FF6B6B'],
            labels={'x': 'Years of Experience', 'y': 'Risk Percentage'}
        )
        fig_exp.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E8E8E8'),
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_exp, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Key Insights
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("💡 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        avg_courses = df['courses_assigned'].mean()
        st.markdown(f"""
            <div class='insight-box'>
                <strong>📚 Average Course Load</strong><br>
                Faculty members teach an average of <strong>{avg_courses:.1f} courses</strong>
            </div>
        """, unsafe_allow_html=True)
        
        avg_hours = df['weekly_teaching_hours'].mean()
        st.markdown(f"""
            <div class='insight-box'>
                <strong>⏰ Average Teaching Hours</strong><br>
                Faculty spend <strong>{avg_hours:.1f} hours/week</strong> teaching
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        high_risk_courses = df[df['workload_risk'] == 1]['courses_assigned'].mean()
        st.markdown(f"""
            <div class='insight-box'>
                <strong>⚠️ High Risk Course Load</strong><br>
                High-risk faculty teach <strong>{high_risk_courses:.1f} courses</strong> on average
            </div>
        """, unsafe_allow_html=True)
        
        high_risk_hours = df[df['workload_risk'] == 1]['weekly_teaching_hours'].mean()
        st.markdown(f"""
            <div class='insight-box'>
                <strong>⚠️ High Risk Teaching Hours</strong><br>
                High-risk faculty work <strong>{high_risk_hours:.1f} hours/week</strong>
            </div>
        """, unsafe_allow_html=True)

# ======================== ANALYTICS ========================
elif selected == "📊 Analytics":
    st.subheader("🔬 Exploratory Data Analysis")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Features", "🔗 Correlations", "📈 Trends", "🎯 Risk Analysis"])
    
    with tab1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        feature = st.selectbox("Select Feature for Analysis", [
            'courses_assigned',
            'weekly_teaching_hours',
            'total_students_handled',
            'admin_roles_count',
            'years_of_experience',
            'preparation_hours_per_week'
        ], key="feature_tab1")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_hist = px.histogram(
                df,
                x=feature,
                color="workload_risk",
                barmode="overlay",
                color_discrete_map={0: '#4ECDC4', 1: '#FF6B6B'},
                labels={'workload_risk': 'Risk Level'}
            )
            fig_hist.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E8E8E8'),
                height=400
            )
            st.plotly_chart(fig_hist, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            fig_box = px.box(
                df,
                x="workload_risk",
                y=feature,
                color="workload_risk",
                color_discrete_map={0: '#4ECDC4', 1: '#FF6B6B'},
                labels={'workload_risk': 'Risk Level'}
            )
            fig_box.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E8E8E8'),
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig_box, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        corr_matrix = df.corr(numeric_only=True)
        fig_corr = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu",
            zmin=-1, zmax=1
        )
        fig_corr.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E8E8E8'),
            height=500
        )
        st.plotly_chart(fig_corr, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        numeric_features = df.select_dtypes(include=[np.number]).columns
        selected_features = st.multiselect("Select Features to Compare", numeric_features, default=['courses_assigned', 'weekly_teaching_hours', 'total_students_handled'])
        
        if selected_features:
            fig_trends = go.Figure()
            for feature in selected_features:
                low_risk_avg = df[df['workload_risk'] == 0][feature].mean()
                high_risk_avg = df[df['workload_risk'] == 1][feature].mean()
                fig_trends.add_trace(go.Bar(
                    name=feature,
                    x=['Low Risk', 'High Risk'],
                    y=[low_risk_avg, high_risk_avg],
                    marker_color=['#4ECDC4', '#FF6B6B'] if feature == selected_features[0] else None
                ))
            fig_trends.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E8E8E8'),
                barmode='group',
                height=400
            )
            st.plotly_chart(fig_trends, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab4:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            students_risk = df.groupby(pd.cut(df['total_students_handled'], bins=5))['workload_risk'].agg(['count', 'sum'])
            students_risk['risk_pct'] = (students_risk['sum'] / students_risk['count'] * 100).round(1)
            
            fig_students = px.bar(
                x=[f"{int(x.left)}-{int(x.right)}" for x in students_risk.index],
                y=students_risk['risk_pct'].values,
                color=students_risk['risk_pct'].values,
                color_continuous_scale=['#4ECDC4', '#FFD93D', '#FF6B6B'],
                labels={'x': 'Students Handled', 'y': 'Risk %'}
            )
            fig_students.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E8E8E8'),
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig_students, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            admin_risk = df.groupby('admin_roles_count')['workload_risk'].apply(lambda x: (x.sum() / len(x) * 100).round(1))
            
            fig_admin = px.bar(
                x=admin_risk.index,
                y=admin_risk.values,
                color=admin_risk.values,
                color_continuous_scale=['#4ECDC4', '#FFD93D', '#FF6B6B'],
                labels={'x': 'Admin Roles', 'y': 'Risk %'}
            )
            fig_admin.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E8E8E8'),
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig_admin, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

# ======================== PREDICTION ========================
elif selected == "🔮 Prediction":
    st.subheader("🤖 Faculty Workload Risk Prediction Engine")
    
    st.markdown("""
        <div class='insight-box'>
            <strong>💡 How it works:</strong> Adjust faculty parameters to predict their workload risk level using our AI model.
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown("### 📋 Faculty Profile")
        st.markdown("<br>", unsafe_allow_html=True)
        
        courses = st.slider("📚 Courses Assigned", 1, 6, 3, help="Number of courses taught")
        weekly_hours = st.slider("⏰ Weekly Teaching Hours", 0, 30, 12, help="Total hours spent teaching per week")
        students = st.slider("👥 Total Students", 10, 300, 100, help="Total number of students taught")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        admin_roles = st.slider("📋 Admin Roles", 0, 5, 1, help="Number of administrative responsibilities")
        experience = st.slider("📅 Years of Experience", 1, 40, 10, help="Years in academia")
        prep_hours = st.slider("📖 Preparation Hours", 0, 20, 5, help="Hours spent on preparation per week")
    
    with col2:
        st.markdown("### 📊 Live Preview")
        
        # Create a nice preview
        preview_data = {
            'Metric': ['Courses', 'Teaching Hours', 'Students', 'Admin Roles', 'Experience', 'Prep Hours'],
            'Value': [courses, f'{weekly_hours}h', students, admin_roles, f'{experience} yrs', f'{prep_hours}h']
        }
        preview_df = pd.DataFrame(preview_data)
        
        fig_preview = go.Figure(data=[go.Table(
            header=dict(
                values=['<b>Metric</b>', '<b>Value</b>'],
                fill_color='rgba(255, 107, 107, 0.3)',
                align='center',
                font=dict(color='#E8E8E8', size=12)
            ),
            cells=dict(
                values=[preview_df['Metric'], preview_df['Value']],
                fill_color='rgba(26, 31, 46, 0.5)',
                align='center',
                font=dict(color='#E8E8E8', size=11)
            )
        )])
        fig_preview.update_layout(
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0)
        )
        st.plotly_chart(fig_preview, use_container_width=True, config={'displayModeBar': False})
    
    # Prediction
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_button = st.button(
            "🔮 PREDICT RISK LEVEL",
            key="predict_btn",
            use_container_width=True
        )
    
    if predict_button:
        # Prepare input
        term_cols = [0, 0, 0, 0]
        exam_cols = [0, 0, 0, 0]
        
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
        prob = model.predict_proba(input_scaled)[0][1]
        prediction = model.predict(input_scaled)[0]
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Result visualization
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if prediction == 1:
                st.markdown("""
                    <div class='risk-high'>
                        <div style='font-size: 2.5em; text-align: center;'>⚠️</div>
                        <div style='font-size: 1.5em; font-weight: 800; text-align: center;'>HIGH RISK</div>
                        <div style='font-size: 0.9em; text-align: center; margin-top: 10px;'>
                            This faculty member shows signs of workload overload
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class='risk-low'>
                        <div style='font-size: 2.5em; text-align: center;'>✅</div>
                        <div style='font-size: 1.5em; font-weight: 800; text-align: center;'>LOW RISK</div>
                        <div style='font-size: 0.9em; text-align: center; margin-top: 10px;'>
                            This faculty member's workload is manageable
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Risk Score Gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Risk Score (%)"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': '#FF6B6B'},
                    'steps': [
                        {'range': [0, 33], 'color': "rgba(78, 205, 196, 0.2)"},
                        {'range': [33, 66], 'color': "rgba(255, 217, 61, 0.2)"},
                        {'range': [66, 100], 'color': "rgba(255, 107, 107, 0.2)"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 50
                    }
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E8E8E8'),
                height=350
            )
            st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
        
        # Recommendations
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("💡 Recommendations")
        
        if prediction == 1:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                    <div class='insight-box'>
                        <strong>✂️ Course Load Reduction</strong><br>
                        Consider reducing the number of courses from """ + str(courses) + """ to """ + str(max(1, courses-1)) + """
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("""
                    <div class='insight-box'>
                        <strong>⏰ Time Management</strong><br>
                        Current teaching load: """ + str(weekly_hours) + """ hours. Target: < 15 hours/week
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("""
                    <div class='insight-box'>
                        <strong>👥 Student Distribution</strong><br>
                        Consider distributing """ + str(students) + """ students across multiple sections
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("""
                    <div class='insight-box'>
                        <strong>📋 Admin Duties</strong><br>
                        Delegate some admin roles to reduce additional stress
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class='insight-box'>
                    <strong>✅ Current workload is well-balanced</strong><br>
                    Keep maintaining this sustainable workload level
                </div>
            """, unsafe_allow_html=True)

# ======================== MODEL COMPARISON ========================
elif selected == "📈 Model Comparison":
    st.subheader("🏆 Machine Learning Model Performance Comparison")
    
    if models_metadata:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        
        # Create comparison data
        comparison_data = []
        for model_name, metadata in models_metadata.items():
            if 'test_metrics' in metadata:
                comparison_data.append({
                    'Model': model_name.upper(),
                    'Accuracy': metadata['test_metrics'].get('accuracy', 0),
                    'Precision': metadata['test_metrics'].get('precision', 0),
                    'Recall': metadata['test_metrics'].get('recall', 0),
                    'F1-Score': metadata['test_metrics'].get('f1_score', 0)
                })
        
        if comparison_data:
            comparison_df = pd.DataFrame(comparison_data)
            
            # Metrics comparison
            col1, col2 = st.columns(2)
            
            with col1:
                metrics_to_plot = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
                fig_metrics = go.Figure()
                
                for metric in metrics_to_plot:
                    fig_metrics.add_trace(go.Scatter(
                        x=comparison_df['Model'],
                        y=comparison_df[metric],
                        mode='lines+markers',
                        name=metric,
                        marker=dict(size=10)
                    ))
                
                fig_metrics.update_layout(
                    title="Performance Metrics Comparison",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#E8E8E8'),
                    height=400,
                    hovermode='x unified'
                )
                st.plotly_chart(fig_metrics, use_container_width=True, config={'displayModeBar': False})
            
            with col2:
                fig_bar = go.Figure()
                
                for metric in metrics_to_plot:
                    fig_bar.add_trace(go.Bar(
                        name=metric,
                        x=comparison_df['Model'],
                        y=comparison_df[metric]
                    ))
                
                fig_bar.update_layout(
                    title="Metric Scores by Model",
                    barmode='group',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#E8E8E8'),
                    height=400
                )
                st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Detailed table
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("📊 Detailed Metrics Table")
            
            # Format for better display
            display_df = comparison_df.copy()
            for col in ['Accuracy', 'Precision', 'Recall', 'F1-Score']:
                display_df[col] = display_df[col].apply(lambda x: f"{x:.4f}")
            
            st.dataframe(display_df, use_container_width=True)
            
            # Model details
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("🔍 Model Details")
            
            selected_model = st.selectbox("Select Model for Details", comparison_df['Model'].tolist())
            model_key = selected_model.lower()
            
            if model_key in models_metadata:
                metadata = models_metadata[model_key]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                        <div class='metric-card'>
                            <div style='font-size: 0.9em; color: #A0A0A0;'>Model Type</div>
                            <div style='font-size: 1.2em; font-weight: 800; color: #FF6B6B;'>{metadata.get('model_type', 'N/A')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    training_records = metadata.get('training_records', 0)
                    st.markdown(f"""
                        <div class='metric-card'>
                            <div style='font-size: 0.9em; color: #A0A0A0;'>Training Records</div>
                            <div style='font-size: 1.2em; font-weight: 800; color: #4ECDC4;'>{training_records}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    num_features = metadata.get('num_features', 0)
                    st.markdown(f"""
                        <div class='metric-card'>
                            <div style='font-size: 0.9em; color: #A0A0A0;'>Features Used</div>
                            <div style='font-size: 1.2em; font-weight: 800; color: #FFD93D;'>{num_features}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Justification
                if 'justification' in metadata:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class='insight-box'>
                            <strong>📝 Why this model?</strong><br>
                            {metadata['justification'].get('reason', 'N/A')}<br><br>
                            <strong>Advantages:</strong>
                            {''.join([f'<br>• {adv}' for adv in metadata['justification'].get('advantages', [])])}
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No model metadata found. Please train models first.")
    else:
        st.info("No models available for comparison.")

# ======================== ABOUT ========================
elif selected == "ℹ️ About":
    st.subheader("ℹ️ About FacultyAI")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
            <div class='insight-box'>
                <h3>🎓 Faculty Workload Risk Prediction System</h3>
                <p>
                    FacultyAI is an intelligent system designed to predict and identify faculty members at risk 
                    of workload overload. By analyzing multiple factors including course load, teaching hours, 
                    student count, and administrative responsibilities, our AI models provide actionable insights 
                    to help institutions maintain sustainable faculty workloads.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
            <div class='insight-box'>
                <h3>📊 Key Metrics Analyzed</h3>
                <ul>
                    <li><strong>Courses Assigned:</strong> Number of courses taught</li>
                    <li><strong>Weekly Teaching Hours:</strong> Total hours spent teaching</li>
                    <li><strong>Total Students:</strong> Number of students taught</li>
                    <li><strong>Admin Roles:</strong> Administrative responsibilities</li>
                    <li><strong>Years of Experience:</strong> Academic experience level</li>
                    <li><strong>Preparation Hours:</strong> Time spent on course preparation</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
            <div class='insight-box'>
                <h3>🤖 AI Models Used</h3>
                <p>
                    Our system employs multiple machine learning models including Logistic Regression, 
                    Decision Trees, Random Forests, SVM, and XGBoost to ensure accurate and robust predictions.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='metric-card' style='text-align: center;'>
                <div style='font-size: 3em; margin: 20px 0;'>🎓</div>
                <div style='font-size: 1.2em; font-weight: 800; color: #FF6B6B; margin: 10px 0;'>FacultyAI</div>
                <div style='font-size: 0.9em; color: #A0A0A0; margin: 10px 0;'>v1.0</div>
                <hr style='border-color: rgba(255, 255, 255, 0.1); margin: 20px 0;'>
                <div style='font-size: 0.85em; color: #A0A0A0;'>
                    <strong>Built with</strong><br>
                    Streamlit • Plotly • Scikit-Learn<br>
                    XGBoost • Pandas • NumPy
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("📈 System Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 1.1em; color: #A0A0A0;'>Total Faculty</div>
                <div style='font-size: 1.8em; font-weight: 800; color: #FF6B6B;'>{len(df)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        high_risk = int(df['workload_risk'].sum())
        st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 1.1em; color: #A0A0A0;'>High Risk</div>
                <div style='font-size: 1.8em; font-weight: 800; color: #FF6B6B;'>{high_risk}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        low_risk = int((df['workload_risk'] == 0).sum())
        st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 1.1em; color: #A0A0A0;'>Low Risk</div>
                <div style='font-size: 1.8em; font-weight: 800; color: #4ECDC4;'>{low_risk}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        models_count = len(models_metadata)
        st.markdown(f"""
            <div class='metric-card'>
                <div style='font-size: 1.1em; color: #A0A0A0;'>ML Models</div>
                <div style='font-size: 1.8em; font-weight: 800; color: #FFD93D;'>{models_count}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='text-align: center; color: #A0A0A0; font-size: 0.9em; margin-top: 40px;'>
            <p>© 2026 FacultyAI. Helping institutions support sustainable faculty workloads.</p>
        </div>
    """, unsafe_allow_html=True)