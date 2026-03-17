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
from datetime import datetime

# ======================== PAGE CONFIG ========================
st.set_page_config(
    page_title="Faculty Workload Intelligence Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================== ADVANCED CUSTOM CSS - GLASSMORPHISM & ANIMATIONS ========================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@600;700;800&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        font-family: 'Inter', sans-serif;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0A0E27 0%, #1a1f3a 50%, #0f1419 100%) !important;
        color: #E8E8E8 !important;
        overflow-x: hidden;
    }
    
    /* ===== GLASSMORPHISM CARDS ===== */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        transform: translateY(-4px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
    }
    
    /* ===== METRIC CARDS - ENHANCED ===== */
    .metric-card-premium {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.1) 0%, rgba(255, 107, 107, 0.05) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 107, 107, 0.2);
        border-radius: 16px;
        padding: 28px;
        box-shadow: 0 8px 32px rgba(255, 107, 107, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card-premium::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .metric-card-premium:hover::before {
        left: 100%;
    }
    
    .metric-card-premium:hover {
        transform: translateY(-6px) scale(1.02);
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.15) 0%, rgba(255, 107, 107, 0.08) 100%);
        border: 1px solid rgba(255, 107, 107, 0.3);
        box-shadow: 0 16px 48px rgba(255, 107, 107, 0.2);
    }
    
    .metric-card-success {
        background: linear-gradient(135deg, rgba(78, 205, 196, 0.1) 0%, rgba(78, 205, 196, 0.05) 100%);
        border: 1px solid rgba(78, 205, 196, 0.2);
        box-shadow: 0 8px 32px rgba(78, 205, 196, 0.1);
    }
    
    .metric-card-success:hover {
        background: linear-gradient(135deg, rgba(78, 205, 196, 0.15) 0%, rgba(78, 205, 196, 0.08) 100%);
        border: 1px solid rgba(78, 205, 196, 0.3);
        box-shadow: 0 16px 48px rgba(78, 205, 196, 0.2);
    }
    
    .metric-card-warning {
        background: linear-gradient(135deg, rgba(255, 217, 61, 0.1) 0%, rgba(255, 217, 61, 0.05) 100%);
        border: 1px solid rgba(255, 217, 61, 0.2);
        box-shadow: 0 8px 32px rgba(255, 217, 61, 0.1);
    }
    
    .metric-card-warning:hover {
        background: linear-gradient(135deg, rgba(255, 217, 61, 0.15) 0%, rgba(255, 217, 61, 0.08) 100%);
        border: 1px solid rgba(255, 217, 61, 0.3);
        box-shadow: 0 16px 48px rgba(255, 217, 61, 0.2);
    }
    
    /* ===== TYPOGRAPHY ===== */
    .title-premium {
        font-family: 'Poppins', sans-serif;
        font-size: 3.2em;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 50%, #FFD93D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
        letter-spacing: -1px;
    }
    
    .subtitle-premium {
        font-size: 1.15em;
        color: #B0B0B0;
        font-weight: 400;
        margin-bottom: 30px;
        letter-spacing: 0.5px;
    }
    
    .section-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.6em;
        font-weight: 700;
        color: #E8E8E8;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    /* ===== CHART CONTAINERS ===== */
    .chart-wrapper {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin: 20px 0;
        transition: all 0.3s ease;
    }
    
    .chart-wrapper:hover {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8787 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 32px !important;
        font-weight: 600 !important;
        font-size: 1em !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 20px rgba(255, 107, 107, 0.3) !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 30px rgba(255, 107, 107, 0.4) !important;
        background: linear-gradient(135deg, #FF8787 0%, #FF6B6B 100%) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* ===== INPUT STYLING ===== */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stMultiSelect > div > div > select {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #E8E8E8 !important;
        border-radius: 12px !important;
        font-size: 1em !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 107, 107, 0.4) !important;
        box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.1) !important;
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] button {
        color: #A0A0A0 !important;
        background-color: transparent !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        border-bottom: 2px solid transparent !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: rgba(255, 107, 107, 0.15) !important;
        color: #FF6B6B !important;
        border-bottom: 2px solid #FF6B6B !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 107, 107, 0.2) !important;
        color: #FF6B6B !important;
        border-bottom: 2px solid #FF6B6B !important;
    }
    
    /* ===== SIDEBAR STYLING ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10, 14, 39, 0.95) 0%, rgba(26, 31, 58, 0.95) 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
    }
    
    /* ===== ALERT BOXES ===== */
    .alert-high-risk {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.25) 0%, rgba(255, 107, 107, 0.15) 100%);
        border: 2px solid rgba(255, 107, 107, 0.4);
        border-radius: 14px;
        padding: 20px;
        color: #FFB3B3;
        font-weight: 500;
        animation: pulse 2s infinite;
    }
    
    .alert-low-risk {
        background: linear-gradient(135deg, rgba(78, 205, 196, 0.25) 0%, rgba(78, 205, 196, 0.15) 100%);
        border: 2px solid rgba(78, 205, 196, 0.4);
        border-radius: 14px;
        padding: 20px;
        color: #A8F0ED;
        font-weight: 500;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-in;
    }
    
    /* ===== INSIGHT BADGES ===== */
    .insight-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(255, 217, 61, 0.2) 0%, rgba(255, 217, 61, 0.1) 100%);
        border: 1px solid rgba(255, 217, 61, 0.3);
        border-radius: 12px;
        padding: 8px 16px;
        color: #FFD93D;
        font-weight: 600;
        font-size: 0.9em;
        margin: 4px 4px 4px 0;
    }
    
    /* ===== DIVIDER ===== */
    .divider-premium {
        height: 1px;
        background: linear-gradient(90deg, 
            rgba(255, 255, 255, 0) 0%, 
            rgba(255, 255, 255, 0.2) 50%, 
            rgba(255, 255, 255, 0) 100%);
        margin: 30px 0;
    }
    
    /* ===== FEATURE IMPORTANCE ===== */
    .feature-bar-container {
        margin: 12px 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .feature-name {
        font-weight: 600;
        color: #E8E8E8;
        min-width: 180px;
        font-size: 0.95em;
    }
    
    .feature-bar {
        flex: 1;
        height: 8px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        overflow: hidden;
        position: relative;
    }
    
    .feature-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #FF6B6B, #FFD93D, #4ECDC4);
        border-radius: 8px;
        transition: width 0.6s ease;
        box-shadow: 0 0 8px rgba(255, 107, 107, 0.4);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.1) 0%, rgba(255, 107, 107, 0.05) 100%);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 107, 107, 0.2);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.2);
    }
    
    .insight-box {
        background: linear-gradient(135deg, rgba(255, 217, 61, 0.1) 0%, rgba(255, 217, 61, 0.05) 100%);
        border-left: 3px solid #FFD93D;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        color: #E8E8E8;
    }
    
    .chart-container {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 15px;
        margin: 15px 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
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
    
    </style>
""", unsafe_allow_html=True)

# ======================== PATHS & DATA LOADING ========================
BASE_DIR = Path(__file__).parent
DATABASE_PATH = BASE_DIR / "data" / "faculty.db"
MODEL_DIR = BASE_DIR / "models"

# Available models
AVAILABLE_MODELS = {
    'logistic': {'path': MODEL_DIR / "logistic_model.joblib", 'scaler': MODEL_DIR / "logistic_scaler.joblib"},
    'random_forest': {'path': MODEL_DIR / "random_forest_model.joblib", 'scaler': None},
    'decision_tree': {'path': MODEL_DIR / "decision_tree_model.joblib", 'scaler': None},
    'xgboost': {'path': MODEL_DIR / "xgboost_model.joblib", 'scaler': None},
}

@st.cache_data
def load_data():
    conn = sqlite3.connect(DATABASE_PATH)
    df = pd.read_sql_query("SELECT * FROM faculty_workload_cleaned", conn)
    conn.close()
    return df

@st.cache_resource
def load_model(model_name='logistic'):
    """Load specified model and its scaler"""
    if model_name not in AVAILABLE_MODELS:
        model_name = 'logistic'
    
    model_config = AVAILABLE_MODELS[model_name]
    model = joblib.load(model_config['path'])
    
    scaler = None
    if model_config['scaler'] and model_config['scaler'].exists():
        scaler = joblib.load(model_config['scaler'])
    
    return model, scaler

@st.cache_data
def load_all_models_metadata():
    metadata = {}
    for model_file in MODEL_DIR.glob("*_metadata.json"):
        with open(model_file) as f:
            metadata[model_file.stem.replace("_metadata", "")] = json.load(f)
    return metadata

df = load_data()
models_metadata = load_all_models_metadata()

# Default model
default_model, default_scaler = load_model('logistic')

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
    <div style='text-align: center; margin: 40px 0 50px 0; padding: 30px; background: linear-gradient(135deg, rgba(255, 107, 107, 0.08) 0%, rgba(78, 205, 196, 0.08) 100%); backdrop-filter: blur(10px); border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1);'>
        <h1 class='title-premium'>🎓 Faculty Workload Intelligence Platform</h1>
        <p class='subtitle-premium'>✨ AI-Powered Predictive Analytics for Faculty Workload Risk Assessment</p>
    </div>
""", unsafe_allow_html=True)

# ======================== DASHBOARD ========================
if selected == "🏠 Dashboard":
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class='metric-card-premium'>
                <div style='font-size: 2.8em; margin-bottom: 12px;'>👥</div>
                <div style='font-size: 0.85em; color: #B0B0B0; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;'>Total Faculty</div>
                <div style='font-size: 2.4em; font-weight: 800; color: #FF6B6B; margin-top: 10px;'>""" + str(len(df)) + """</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        high_risk = int(df['workload_risk'].sum())
        st.markdown(f"""
            <div class='metric-card-premium' style='background: linear-gradient(135deg, rgba(255, 107, 107, 0.15) 0%, rgba(255, 107, 107, 0.08) 100%); border: 1px solid rgba(255, 107, 107, 0.3);'>
                <div style='font-size: 2.8em; margin-bottom: 12px;'>⚠️</div>
                <div style='font-size: 0.85em; color: #FFB3B3; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;'>High Risk <span style='font-size: 0.7em;'>(🔴)</span></div>
                <div style='font-size: 2.4em; font-weight: 800; color: #FF6B6B; margin-top: 10px;'>{high_risk}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        low_risk = int((df['workload_risk'] == 0).sum())
        st.markdown(f"""
            <div class='metric-card-success'>
                <div style='font-size: 2.8em; margin-bottom: 12px;'>✅</div>
                <div style='font-size: 0.85em; color: #A8F0ED; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;'>Low Risk <span style='font-size: 0.7em;'>(✓)</span></div>
                <div style='font-size: 2.4em; font-weight: 800; color: #4ECDC4; margin-top: 10px;'>{low_risk}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        risk_percentage = round((high_risk / len(df)) * 100, 1)
        st.markdown(f"""
            <div class='metric-card-warning'>
                <div style='font-size: 2.8em; margin-bottom: 12px;'>📊</div>
                <div style='font-size: 0.85em; color: #FFE899; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;'>Overall Risk Rate</div>
                <div style='font-size: 2.4em; font-weight: 800; color: #FFD93D; margin-top: 10px;'>{risk_percentage}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='chart-wrapper' style='animation: fadeIn 0.6s ease;'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📊 Risk Distribution</div>", unsafe_allow_html=True)
        fig_pie = px.pie(
            values=[low_risk, high_risk],
            names=['Low Risk', 'High Risk'],
            color_discrete_sequence=['#4ECDC4', '#FF6B6B'],
            hole=0.3
        )
        fig_pie.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E8E8E8', family='Poppins'),
            height=400
        )
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='chart-wrapper' style='animation: fadeIn 0.7s ease;'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📈 Risk by Experience Level</div>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-title'>💡 Key Insights & Statistics</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        avg_courses = df['courses_assigned'].mean()
        st.markdown(f"""
            <div class='insight-box'>
                <strong>📚 Average Course Load</strong><br>
                Faculty teach <strong>{avg_courses:.1f} courses</strong> on average<br>
                <span style='color: #A0A0A0; font-size: 0.85em;'>Range: {int(df['courses_assigned'].min())}-{int(df['courses_assigned'].max())} courses</span>
            </div>
        """, unsafe_allow_html=True)
        
        avg_hours = df['weekly_teaching_hours'].mean()
        st.markdown(f"""
            <div class='insight-box'>
                <strong>⏰ Average Teaching Hours</strong><br>
                Faculty spend <strong>{avg_hours:.1f} hours/week</strong> teaching<br>
                <span style='color: #A0A0A0; font-size: 0.85em;'>Range: {int(df['weekly_teaching_hours'].min())}-{int(df['weekly_teaching_hours'].max())} hours</span>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        high_risk_courses = df[df['workload_risk'] == 1]['courses_assigned'].mean()
        st.markdown(f"""
            <div class='insight-box'>
                <strong>⚠️ High Risk Course Load</strong><br>
                High-risk faculty teach <strong>{high_risk_courses:.1f} courses</strong> (vs {df[df['workload_risk'] == 0]['courses_assigned'].mean():.1f} for low-risk)<br>
                <span style='color: #A0A0A0; font-size: 0.85em;'>Difference: +{high_risk_courses - df[df['workload_risk'] == 0]['courses_assigned'].mean():.1f} courses</span>
            </div>
        """, unsafe_allow_html=True)
        
        high_risk_hours = df[df['workload_risk'] == 1]['weekly_teaching_hours'].mean()
        st.markdown(f"""
            <div class='insight-box'>
                <strong>⚠️ High Risk Teaching Hours</strong><br>
                High-risk faculty work <strong>{high_risk_hours:.1f} hours/week</strong> (vs {df[df['workload_risk'] == 0]['weekly_teaching_hours'].mean():.1f} for low-risk)<br>
                <span style='color: #A0A0A0; font-size: 0.85em;'>Difference: +{high_risk_hours - df[df['workload_risk'] == 0]['weekly_teaching_hours'].mean():.1f} hours</span>
            </div>
        """, unsafe_allow_html=True)
    
    # Additional analysis tabs
    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📊 Detailed Breakdown", "🎯 Risk Factors", "💼 Experience Impact"])
    
    with tab1:
        st.markdown("<div class='chart-wrapper' style='animation: fadeIn 0.6s ease;'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            # Courses distribution
            fig_courses = px.box(
                df,
                y='courses_assigned',
                color='workload_risk',
                color_discrete_map={0: '#4ECDC4', 1: '#FF6B6B'},
                labels={'workload_risk': 'Risk Level', 'courses_assigned': 'Courses'},
                points='all'
            )
            fig_courses.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E8E8E8'),
                height=350,
                showlegend=False
            )
            st.plotly_chart(fig_courses, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            # Teaching hours distribution
            fig_hours = px.box(
                df,
                y='weekly_teaching_hours',
                color='workload_risk',
                color_discrete_map={0: '#4ECDC4', 1: '#FF6B6B'},
                labels={'workload_risk': 'Risk Level', 'weekly_teaching_hours': 'Hours/Week'},
                points='all'
            )
            fig_hours.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E8E8E8'),
                height=350,
                showlegend=False
            )
            st.plotly_chart(fig_hours, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<div class='chart-wrapper' style='animation: fadeIn 0.7s ease;'>", unsafe_allow_html=True)
        
        # Identify key risk factors
        col1, col2 = st.columns(2)
        
        with col1:
            # Students handled vs risk
            fig_students = px.scatter(
                df,
                x='total_students_handled',
                y='weekly_teaching_hours',
                color='workload_risk',
                size='courses_assigned',
                color_discrete_map={0: '#4ECDC4', 1: '#FF6B6B'},
                labels={'total_students_handled': 'Total Students', 'weekly_teaching_hours': 'Teaching Hours/Week'},
                title='Student Load vs Teaching Hours'
            )
            fig_students.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E8E8E8'),
                height=350
            )
            st.plotly_chart(fig_students, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            # Admin roles impact
            admin_risk = df.groupby('admin_roles_count').agg({
                'workload_risk': ['count', 'sum'],
                'weekly_teaching_hours': 'mean'
            }).round(2)
            admin_risk.columns = ['Total', 'High Risk', 'Avg Teaching Hours']
            admin_risk['Risk %'] = (admin_risk['High Risk'] / admin_risk['Total'] * 100).round(1)
            
            fig_admin = px.bar(
                x=admin_risk.index,
                y=admin_risk['Risk %'],
                color=admin_risk['Risk %'],
                color_continuous_scale=['#4ECDC4', '#FFD93D', '#FF6B6B'],
                labels={'x': 'Admin Roles', 'y': 'Risk %'}
            )
            fig_admin.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E8E8E8'),
                height=350,
                showlegend=False,
                title='Risk Rate by Admin Responsibilities'
            )
            st.plotly_chart(fig_admin, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown("<div class='chart-wrapper' style='animation: fadeIn 0.8s ease;'>", unsafe_allow_html=True)
        
        # Experience vs workload
        col1, col2 = st.columns(2)
        
        with col1:
            experience_risk = df.groupby(pd.cut(df['years_of_experience'], bins=5))['workload_risk'].agg(['count', 'sum']).round(0)
            experience_risk.columns = ['Total', 'High Risk']
            experience_risk['Risk %'] = (experience_risk['High Risk'] / experience_risk['Total'] * 100).round(1)
            
            fig_exp = px.bar(
                x=[f"{int(x.left)}-{int(x.right)}" for x in experience_risk.index],
                y=experience_risk['Risk %'].values,
                color=experience_risk['Risk %'].values,
                color_continuous_scale=['#4ECDC4', '#FFD93D', '#FF6B6B'],
                labels={'x': 'Years of Experience', 'y': 'Risk %'},
                title='Risk by Experience Level'
            )
            fig_exp.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E8E8E8'),
                height=350,
                showlegend=False
            )
            st.plotly_chart(fig_exp, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            # Preparation hours matter
            st.markdown("""
                <div class='insight-box'>
                    <strong>📖 Preparation Time Impact</strong>
                </div>
            """, unsafe_allow_html=True)
            
            prep_stats = df.groupby('workload_risk')[['preparation_hours_per_week', 'weekly_teaching_hours', 'courses_assigned']].mean().round(1)
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown(f"""
                    <div style='background: rgba(78, 205, 196, 0.1); border-left: 3px solid #4ECDC4; padding: 10px; border-radius: 5px;'>
                        <div style='font-size: 0.9em; color: #A0A0A0;'><strong>Low Risk Faculty</strong></div>
                        <div style='font-size: 0.85em; color: #E8E8E8; margin-top: 5px;'>
                            Prep Hours: {prep_stats.loc[0, 'preparation_hours_per_week']:.1f}/week<br>
                            Teaching Hours: {prep_stats.loc[0, 'weekly_teaching_hours']:.1f}/week<br>
                            Courses: {prep_stats.loc[0, 'courses_assigned']:.1f}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                st.markdown(f"""
                    <div style='background: rgba(255, 107, 107, 0.1); border-left: 3px solid #FF6B6B; padding: 10px; border-radius: 5px;'>
                        <div style='font-size: 0.9em; color: #A0A0A0;'><strong>High Risk Faculty</strong></div>
                        <div style='font-size: 0.85em; color: #E8E8E8; margin-top: 5px;'>
                            Prep Hours: {prep_stats.loc[1, 'preparation_hours_per_week']:.1f}/week<br>
                            Teaching Hours: {prep_stats.loc[1, 'weekly_teaching_hours']:.1f}/week<br>
                            Courses: {prep_stats.loc[1, 'courses_assigned']:.1f}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ======================== ANALYTICS ========================
elif selected == "📊 Analytics":
    st.markdown("<div class='section-title'>🔬 Exploratory Data Analysis</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Features", "🔗 Correlations", "📈 Trends", "🎯 Risk Analysis"])
    
    with tab1:
        st.markdown("<div class='chart-wrapper' style='animation: fadeIn 0.6s ease;'>", unsafe_allow_html=True)
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
        st.markdown("<div class='chart-wrapper' style='animation: fadeIn 0.6s ease;'>", unsafe_allow_html=True)
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
        st.markdown("<div class='chart-wrapper' style='animation: fadeIn 0.7s ease;'>", unsafe_allow_html=True)
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
        st.markdown("<div class='chart-wrapper' style='animation: fadeIn 0.8s ease;'>", unsafe_allow_html=True)
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
    st.markdown("<div class='section-title'>🤖 Faculty Workload Risk Prediction Engine</div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='insight-box' style='border-left: 4px solid #FFD93D; background: linear-gradient(135deg, rgba(255, 217, 61, 0.15) 0%, rgba(255, 217, 61, 0.08) 100%);'>
            <strong>💡 How it works:</strong> Enter faculty details below to predict workload risk with our advanced AI model.
        </div>
    """, unsafe_allow_html=True)
    
    # Model Selection
    st.markdown("<div class='section-title' style='font-size: 1.25em; margin-top: 30px;'>🤖 Select Prediction Model</div>", unsafe_allow_html=True)
    model_col1, model_col2, model_col3 = st.columns(3)
    
    with model_col1:
        selected_model_name = st.selectbox(
            "Choose Model:",
            ['Logistic Regression', 'Random Forest', 'Decision Tree', 'XGBoost'],
            help="Different models may give different predictions"
        )
        
        model_key = selected_model_name.lower().replace(' ', '_')
        if 'logistic' in model_key:
            model_key = 'logistic'
        elif 'random' in model_key:
            model_key = 'random_forest'
        elif 'decision' in model_key:
            model_key = 'decision_tree'
        elif 'xgboost' in model_key:
            model_key = 'xgboost'
        
        # Load selected model
        selected_model, selected_scaler = load_model(model_key)
    
    # Show model info
    with model_col2:
        if model_key in models_metadata:
            meta = models_metadata[model_key]
            accuracy = meta.get('test_metrics', {}).get('accuracy', 'N/A')
            st.markdown(f"""
                <div style='text-align: center; padding: 10px; background: rgba(255, 107, 107, 0.1); border-radius: 8px;'>
                    <div style='font-size: 0.85em; color: #A0A0A0;'>Model Accuracy</div>
                    <div style='font-size: 1.4em; font-weight: 800; color: #4ECDC4;'>{accuracy if isinstance(accuracy, str) else f"{accuracy:.2%}"}</div>
                </div>
            """, unsafe_allow_html=True)
    
    with model_col3:
        if model_key in models_metadata:
            meta = models_metadata[model_key]
            f1 = meta.get('test_metrics', {}).get('f1_score', 'N/A')
            st.markdown(f"""
                <div style='text-align: center; padding: 10px; background: rgba(78, 205, 196, 0.1); border-radius: 8px;'>
                    <div style='font-size: 0.85em; color: #A0A0A0;'>F1-Score</div>
                    <div style='font-size: 1.4em; font-weight: 800; color: #FFD93D;'>{f1 if isinstance(f1, str) else f"{f1:.4f}"}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: rgba(255, 255, 255, 0.1); margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Helper statistics from data
    avg_courses = df['courses_assigned'].mean()
    avg_hours = df['weekly_teaching_hours'].mean()
    avg_students = df['total_students_handled'].mean()
    avg_prep = df['preparation_hours_per_week'].mean()
    
    col1, col2 = st.columns([1.2, 1.8])
    
    with col1:
        st.markdown("<div class='section-title' style='font-size: 1.25em; margin-bottom: 20px;'>📋 Faculty Profile</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Use compact number inputs with columns for space efficiency
        input_col1, input_col2 = st.columns(2)
        
        with input_col1:
            courses = st.number_input(
                "📚 Courses",
                min_value=1,
                max_value=6,
                value=3,
                help=f"Avg: {avg_courses:.1f}"
            )
        
        with input_col2:
            admin_roles = st.number_input(
                "📋 Admin Roles",
                min_value=0,
                max_value=5,
                value=1,
                help="0-5 roles"
            )
        
        input_col1, input_col2 = st.columns(2)
        
        with input_col1:
            weekly_hours = st.number_input(
                "⏰ Teaching Hours",
                min_value=0,
                max_value=30,
                value=12,
                step=1,
                help=f"Weekly hours (Avg: {avg_hours:.1f})"
            )
        
        with input_col2:
            experience = st.number_input(
                "📅 Experience",
                min_value=1,
                max_value=40,
                value=10,
                step=1,
                help="Years in academia"
            )
        
        input_col1, input_col2 = st.columns(2)
        
        with input_col1:
            students = st.number_input(
                "👥 Students",
                min_value=10,
                max_value=300,
                value=100,
                step=10,
                help=f"Total students (Avg: {avg_students:.0f})"
            )
        
        with input_col2:
            prep_hours = st.number_input(
                "📖 Prep Hours",
                min_value=0,
                max_value=20,
                value=5,
                step=1,
                help=f"Weekly prep hrs (Avg: {avg_prep:.1f})"
            )
        
        st.markdown("<hr style='border-color: rgba(255, 255, 255, 0.1); margin: 15px 0;'>", unsafe_allow_html=True)
        
        # Faculty workload summary
        total_load = (courses * 3) + weekly_hours + prep_hours
        st.markdown(f"""
            <div style='background: rgba(255, 107, 107, 0.1); border-left: 3px solid #FF6B6B; padding: 10px; border-radius: 5px; margin: 10px 0;'>
                <div style='font-size: 0.85em; color: #A0A0A0;'>Total Work Units</div>
                <div style='font-size: 1.4em; font-weight: 800; color: #FFD93D;'>{total_load}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='section-title' style='font-size: 1.25em; margin-bottom: 20px;'>📊 Comparative Analysis</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Compare with dataset averages
        comparison_data = {
            'Parameter': ['Courses', 'Teaching Hrs', 'Students', 'Admin Roles', 'Experience', 'Prep Hours'],
            'Your Input': [courses, weekly_hours, students, admin_roles, experience, prep_hours],
            'Dataset Avg': [
                f"{avg_courses:.1f}",
                f"{avg_hours:.1f}",
                f"{avg_students:.0f}",
                "1.2",
                "12.5",
                f"{avg_prep:.1f}"
            ]
        }
        
        comp_df = pd.DataFrame(comparison_data)
        
        st.markdown("**📈 How you compare to other faculty:**")
        
        # Comparison visualization
        col_comp1, col_comp2 = st.columns([1, 1])
        
        with col_comp1:
            # Courses comparison
            fig_comp1 = go.Figure(data=[
                go.Bar(name='Your Load', x=['Courses'], y=[courses], marker_color='#FF6B6B'),
                go.Bar(name='Average', x=['Courses'], y=[avg_courses], marker_color='#4ECDC4')
            ])
            fig_comp1.update_layout(height=250, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                                   font=dict(color='#E8E8E8'), showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig_comp1, use_container_width=True, config={'displayModeBar': False})
        
        with col_comp2:
            # Teaching hours comparison
            fig_comp2 = go.Figure(data=[
                go.Bar(name='Your Load', x=['Teaching Hours'], y=[weekly_hours], marker_color='#FF6B6B'),
                go.Bar(name='Average', x=['Teaching Hours'], y=[avg_hours], marker_color='#4ECDC4')
            ])
            fig_comp2.update_layout(height=250, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                                   font=dict(color='#E8E8E8'), showlegend=False, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig_comp2, use_container_width=True, config={'displayModeBar': False})
        
        # Risk factors display
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**⚠️ Risk Factors Assessment:**")
        
        risk_factors = []
        if courses >= 5:
            risk_factors.append("🔴 High course load (5+ courses)")
        if weekly_hours >= 20:
            risk_factors.append("🔴 High teaching hours (20+ hrs/week)")
        if students >= 200:
            risk_factors.append("🟡 Large student population (200+ students)")
        if admin_roles >= 3:
            risk_factors.append("🟡 Multiple admin roles (3+ roles)")
        if prep_hours <= 3:
            risk_factors.append("🟠 Low preparation time")
        
        if risk_factors:
            for factor in risk_factors:
                st.markdown(f"<div style='color: #E8E8E8; font-size: 0.9em; margin: 3px 0;'>{factor}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='color: #4ECDC4; font-size: 0.9em;'>✅ No major risk factors detected</div>", unsafe_allow_html=True)
    
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
        
        # Scale input if scaler available
        if selected_scaler:
            input_scaled = selected_scaler.transform(input_data)
        else:
            input_scaled = input_data
        
        # Get predictions from selected model
        prob = selected_model.predict_proba(input_scaled)[0][1]
        prediction = selected_model.predict(input_scaled)[0]
        
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
                mode="gauge+number+delta",
                value=prob * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Risk Score (%)"},
                delta={'reference': 50},
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
                height=300
            )
            st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
        
        # Detailed Analysis
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title' style='font-size: 1.25em; margin-bottom: 20px;'>📊 Detailed Risk Analysis</div>", unsafe_allow_html=True)
        
        # Calculate risk metrics
        risk_score = prob * 100
        workload_index = (courses * 15) + (weekly_hours * 2) + (students / 20) + (prep_hours * 3)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 0.85em; color: #A0A0A0;'>Risk Probability</div>
                    <div style='font-size: 1.6em; font-weight: 800; color: #FF6B6B;'>{risk_score:.1f}%</div>
                    <div style='font-size: 0.75em; color: #A0A0A0; margin-top: 5px;'>
                        {"High" if risk_score > 50 else "Low"} Risk
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 0.85em; color: #A0A0A0;'>Workload Index</div>
                    <div style='font-size: 1.6em; font-weight: 800; color: #4ECDC4;'>{workload_index:.0f}</div>
                    <div style='font-size: 0.75em; color: #A0A0A0; margin-top: 5px;'>
                        {"Heavy" if workload_index > 200 else "Moderate" if workload_index > 100 else "Light"}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            efficiency = (prep_hours / (weekly_hours + 1)) * 100
            st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 0.85em; color: #A0A0A0;'>Prep Efficiency</div>
                    <div style='font-size: 1.6em; font-weight: 800; color: #FFD93D;'>{efficiency:.0f}%</div>
                    <div style='font-size: 0.75em; color: #A0A0A0; margin-top: 5px;'>
                        {"Good" if efficiency > 30 else "Needs attention"}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            student_per_course = students / courses if courses > 0 else 0
            st.markdown(f"""
                <div class='metric-card'>
                    <div style='font-size: 0.85em; color: #A0A0A0;'>Avg Students/Course</div>
                    <div style='font-size: 1.6em; font-weight: 800; color: #4ECDC4;'>{student_per_course:.0f}</div>
                    <div style='font-size: 0.75em; color: #A0A0A0; margin-top: 5px;'>
                        Per course load
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # Recommendations
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title' style='font-size: 1.25em; margin-bottom: 20px;'>💡 Personalized Recommendations</div>", unsafe_allow_html=True)
        
        recommendations = []
        
        # Generate smart recommendations based on data
        if courses >= 5:
            recommendations.append(("✂️ Reduce Course Load", f"Consider teaching {max(1, courses-1)} courses instead of {courses} to focus on quality."))
        
        if weekly_hours >= 20:
            recommendations.append(("⏰ Optimize Teaching Time", f"Your teaching load is {weekly_hours} hours/week. Target: 12-15 hours/week."))
        
        if students >= 200:
            recommendations.append(("👥 Distribute Students", f"Break down your {students} students into smaller sections for better engagement."))
        
        if admin_roles >= 3:
            recommendations.append(("📋 Delegate Admin Duties", "Consider delegating some administrative responsibilities to colleagues."))
        
        if prep_hours <= 3 and (courses >= 3 or weekly_hours >= 15):
            recommendations.append(("📖 Increase Prep Time", "Allocate more time for course preparation and grading."))
        
        if experience < 5 and courses >= 4:
            recommendations.append(("🎓 Mentor Support", "As a newer faculty, consider reducing course load to 3-4 courses."))
        
        if not recommendations:
            st.markdown("""
                <div class='insight-box' style='text-align: center;'>
                    <strong>✅ Your workload appears well-balanced!</strong><br>
                    Continue maintaining this sustainable pace and focus on quality education.
                </div>
            """, unsafe_allow_html=True)
        else:
            for idx, (title, desc) in enumerate(recommendations, 1):
                col = st.columns(1)[0]
                st.markdown(f"""
                    <div class='insight-box'>
                        <strong>{title}</strong><br>
                        {desc}
                    </div>
                """, unsafe_allow_html=True)
        
        # Comparative insights
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title' style='font-size: 1.25em; margin-bottom: 20px;'>📈 Comparative Insights</div>", unsafe_allow_html=True)
        
        # Find similar faculty from dataset
        similar_faculty = df[
            (df['courses_assigned'] == courses) &
            (df['admin_roles_count'] == admin_roles)
        ]
        
        if len(similar_faculty) > 0:
            similar_risk = similar_faculty['workload_risk'].sum()
            similar_total = len(similar_faculty)
            similar_risk_pct = (similar_risk / similar_total * 100).round(1) if similar_total > 0 else 0
            
            st.markdown(f"""
                <div class='insight-box'>
                    <strong>🔍 Similar Faculty Profile Found</strong><br>
                    Found {similar_total} faculty with {courses} courses and {admin_roles} admin roles<br>
                    Risk rate among them: <strong>{similar_risk_pct}%</strong> (Your risk: <strong>{risk_score:.1f}%</strong>)
                </div>
            """, unsafe_allow_html=True)
        
        # Comparison with high vs low risk groups
        col1, col2 = st.columns(2)
        
        with col1:
            high_risk_df = df[df['workload_risk'] == 1]
            if len(high_risk_df) > 0:
                st.markdown(f"""
                    <div class='insight-box'>
                        <strong>⚠️ High Risk Faculty Average</strong><br>
                        Courses: {high_risk_df['courses_assigned'].mean():.1f}<br>
                        Teaching Hours: {high_risk_df['weekly_teaching_hours'].mean():.1f}/week<br>
                        Students: {high_risk_df['total_students_handled'].mean():.0f}
                    </div>
                """, unsafe_allow_html=True)
        
        with col2:
            low_risk_df = df[df['workload_risk'] == 0]
            if len(low_risk_df) > 0:
                st.markdown(f"""
                    <div class='insight-box'>
                        <strong>✅ Low Risk Faculty Average</strong><br>
                        Courses: {low_risk_df['courses_assigned'].mean():.1f}<br>
                        Teaching Hours: {low_risk_df['weekly_teaching_hours'].mean():.1f}/week<br>
                        Students: {low_risk_df['total_students_handled'].mean():.0f}
                    </div>
                """, unsafe_allow_html=True)
        
        # All Models Predictions Comparison
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-title' style='font-size: 1.25em; margin-bottom: 20px;'>🎯 All Models Predictions</div>", unsafe_allow_html=True)
        
        all_predictions = []
        for model_name in ['logistic', 'random_forest', 'decision_tree', 'xgboost']:
            try:
                m, s = load_model(model_name)
                if s:
                    inp_scaled = s.transform(input_data)
                else:
                    inp_scaled = input_data
                
                pred_prob = m.predict_proba(inp_scaled)[0][1]
                pred = m.predict(inp_scaled)[0]
                
                # Get model accuracy
                model_accuracy = 0.0
                if model_name in models_metadata:
                    model_accuracy = models_metadata[model_name].get('test_metrics', {}).get('accuracy', 0.0)
                
                all_predictions.append({
                    'Model': model_name.replace('_', ' ').title(),
                    'Risk %': f"{pred_prob*100:.1f}%",
                    'Prediction': '🔴 HIGH RISK' if pred == 1 else '✅ LOW RISK',
                    'Accuracy': f"{model_accuracy:.1%}",
                    'Confidence': pred_prob * 100
                })
            except:
                pass
        
        if all_predictions:
            pred_df = pd.DataFrame(all_predictions)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # Table of all predictions
                display_df = pred_df[['Model', 'Risk %', 'Prediction', 'Accuracy']].copy()
                st.dataframe(display_df, use_container_width=True)
            
            with col2:
                # Visualization of confidence scores
                fig_consensus = go.Figure(data=[
                    go.Bar(
                        y=pred_df['Model'],
                        x=pred_df['Confidence'],
                        orientation='h',
                        marker=dict(
                            color=pred_df['Confidence'],
                            colorscale=['#4ECDC4', '#FFD93D', '#FF6B6B'],
                            showscale=False
                        )
                    )
                ])
                fig_consensus.update_layout(
                    title="Model Consensus",
                    xaxis_title="Risk Confidence (%)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#E8E8E8'),
                    height=350,
                    margin=dict(l=80)
                )
                st.plotly_chart(fig_consensus, use_container_width=True, config={'displayModeBar': False})

# ======================== MODEL COMPARISON ========================
elif selected == "📈 Model Comparison":
    st.markdown("<div class='section-title'>🏆 Machine Learning Model Performance Comparison</div>", unsafe_allow_html=True)
    
    if models_metadata:
        st.markdown("<div class='chart-wrapper' style='animation: fadeIn 0.6s ease;'>", unsafe_allow_html=True)
        
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
                    font=dict(color='#E8E8E8', family='Poppins'),
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
            st.markdown("<div class='section-title' style='font-size: 1.1em; margin-bottom: 15px;'>📊 Detailed Metrics Table</div>", unsafe_allow_html=True)
            
            # Format for better display
            display_df = comparison_df.copy()
            for col in ['Accuracy', 'Precision', 'Recall', 'F1-Score']:
                display_df[col] = display_df[col].apply(lambda x: f"{x:.4f}")
            
            st.dataframe(display_df, use_container_width=True)
            
            # Model details
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<div class='section-title' style='font-size: 1.1em; margin-bottom: 15px;'>🔍 Model Details</div>", unsafe_allow_html=True)
            
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
    st.markdown("<div class='section-title'>ℹ️ About FacultyAI</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
            <div class='insight-box' style='border-left: 4px solid #4ECDC4; background: linear-gradient(135deg, rgba(78, 205, 196, 0.15) 0%, rgba(78, 205, 196, 0.08) 100%);'>
                <h3 style='color: #4ECDC4; font-family: Poppins;'>🎓 Faculty Workload Intelligence Platform</h3>
                <p style='color: #E8E8E8; line-height: 1.6;'>
                    FacultyAI is an intelligent system designed to predict and identify faculty members at risk 
                    of workload overload. By analyzing multiple factors including course load, teaching hours, 
                    student count, and administrative responsibilities, our AI models provide actionable insights 
                    to help institutions maintain sustainable faculty workloads.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
            <div class='insight-box' style='border-left: 4px solid #FF6B6B; background: linear-gradient(135deg, rgba(255, 107, 107, 0.15) 0%, rgba(255, 107, 107, 0.08) 100%);'>
                <h3 style='color: #FF6B6B; font-family: Poppins;'>📊 Key Metrics Analyzed</h3>
                <ul style='color: #E8E8E8; line-height: 1.8;'>
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
            <div class='insight-box' style='border-left: 4px solid #FFD93D;'>
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
    
    st.markdown("<div class='section-title'>📈 System Statistics</div>", unsafe_allow_html=True)
    
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