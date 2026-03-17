# 🎓 Faculty Workload Risk Prediction System

## Overview

**FacultyAI** is an intelligent, AI-powered system designed to predict and identify faculty members at risk of workload overload in educational institutions. This system analyzes multiple factors including course load, teaching hours, student count, and administrative responsibilities to provide actionable insights and help institutions maintain sustainable faculty workloads.

## 🎯 Problem Statement

Faculty workload management is a critical challenge in educational institutions. Excessive workloads can lead to:
- Decreased teaching quality
- Faculty burnout and stress
- Higher attrition rates
- Reduced research productivity
- Work-life balance issues

**FacultyAI** provides data-driven insights to identify at-risk faculty and recommend interventions before burnout occurs.

---

## ✨ Key Features

### 📊 Interactive Dashboard
- **Real-time Analytics** - Explore faculty workload patterns and risks
- **Multiple Visualizations** - Interactive Plotly charts and advanced analytics
- **Responsive Design** - Works seamlessly on desktop and mobile devices
- **Professional UI** - Dark mode with attractive gradient backgrounds

### 🔮 Prediction Engine
- **Multi-Model Support** - Choose between 4 different AI models:
  - Logistic Regression (Fast & Interpretable)
  - Random Forest (Strong Ensemble)
  - Decision Tree (Explainable)
  - XGBoost (High-Performance)
- **Compact Input Form** - Number inputs reduce scrolling and save space
- **Real-time Comparisons** - See how faculty data compares to dataset averages
- **Risk Factor Assessment** - Identify specific risk factors in the workload

### 📈 Detailed Analysis
- **Workload Index Calculation** - Comprehensive metric combining all factors
- **Preparedness Efficiency Score** - Measure preparation time vs teaching load
- **Risk Metrics** - Probability, confidence scores, and detailed breakdowns
- **Personalized Recommendations** - AI-generated suggestions based on risk factors

### 📊 Analytics Suite
- **EDA Analysis** - Exploratory data analysis with 4 advanced tabs
- **Feature Breakdown** - Distributions and comparative visualizations
- **Risk Factor Analysis** - Student load and administrative impact
- **Experience Impact** - How seniority affects workload risk

### 🏆 Model Comparison
- **Performance Metrics** - Compare accuracy, precision, recall, F1-score
- **Visual Comparisons** - Line and bar charts for easy comparison
- **Model Details** - Learn why each model works and its advantages
- **Feature Importance** - Understand what factors matter most

---

## 📋 Dataset Information

### Data Source
- **Database**: SQLite (`faculty.db`)
- **Table**: `faculty_workload_cleaned`
- **Records**: 96 faculty members
- **Features**: 14 variables

### Features Used
| Feature | Type | Description |
|---------|------|-------------|
| `courses_assigned` | Numeric | Number of courses taught (1-6) |
| `weekly_teaching_hours` | Numeric | Total teaching hours per week (0-30) |
| `total_students_handled` | Numeric | Total number of students taught (10-300) |
| `admin_roles_count` | Numeric | Number of administrative roles (0-5) |
| `years_of_experience` | Numeric | Years in academia (1-40) |
| `preparation_hours_per_week` | Numeric | Weekly preparation hours (0-20) |
| `term_*` | Categorical | Encoding for academic terms (Colors, Festival, Independence, Republic) |
| `exam_*` | Categorical | Encoding for exam types (End Term, Mid Term, Unit Test 1, Unit Test 2) |
| `workload_risk` | Target | 0=Low Risk, 1=High Risk |

### Data Statistics
- **Total Faculty**: 96
- **High Risk**: 22 faculty (23%)
- **Low Risk**: 74 faculty (77%)
- **Average Course Load**: 3.2 courses
- **Average Teaching Hours**: 13.5 hours/week

---

## 🤖 Machine Learning Models

### Models Implemented

#### 1. **Logistic Regression** ⚡
- **Status**: ✅ Active
- **Type**: Linear Classification
- **Accuracy**: ~79%
- **Advantages**: Fast, interpretable, probability-based predictions
- **Best For**: Quick baseline and understanding feature importance

#### 2. **Random Forest** 🌲
- **Status**: ✅ Active
- **Type**: Ensemble (Multiple Decision Trees)
- **Accuracy**: ~88%
- **Advantages**: Handles non-linearity, robust to outliers, feature importance
- **Best For**: Balanced accuracy and interpretability

#### 3. **Decision Tree** 🌳
- **Status**: ✅ Active
- **Type**: Tree-based Classification
- **Accuracy**: ~79%
- **Advantages**: Highly interpretable, easy to visualize decision logic
- **Best For**: Understanding decision pathways and rules

#### 4. **XGBoost** 🚀
- **Status**: ✅ Active
- **Type**: Gradient Boosting
- **Accuracy**: 87.5%
- **Advantages**: Highest performance, handles complex patterns, feature interactions
- **Best For**: Production predictions and maximum accuracy

### Model Performance Comparison

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| Logistic Regression | 0.79 | 0.75 | 0.45 | 0.57 |
| Random Forest | 0.88 | 1.00 | 0.64 | 0.78 |
| Decision Tree | 0.79 | 0.64 | 0.45 | 0.53 |
| XGBoost | 0.875 | 1.00 | 0.50 | 0.67 |

---

## 🛠️ Technologies Used

### Backend & Data Processing
- **Python 3.13** - Core programming language
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computations
- **SQLite3** - Database management

### Machine Learning
- **Scikit-Learn** - ML algorithms (Logistic Regression, Random Forest, Decision Tree)
- **XGBoost** - Gradient boosting library
- **Joblib** - Model serialization and loading

### Frontend & Visualization
- **Streamlit** - Interactive web application framework
- **Streamlit-option-menu** - Enhanced navigation menu
- **Plotly** - Interactive visualizations and charts

### Version Control
- **Git** - Version control system
- **GitHub** - Remote repository hosting

---

## 📁 Project Structure

```
faculty-risk-prediction/
│
├── app.py                          # Main Streamlit application
│
├── data/
│   ├── faculty.db                  # SQLite database with faculty data
│   ├── cleaning_report.json        # Data cleaning logs
│   └── generation_metadata.json    # Data generation details
│
├── models/
│   ├── logistic_model.joblib       # Trained Logistic Regression model
│   ├── logistic_scaler.joblib      # Logistic Regression scaler
│   ├── random_forest_model.joblib  # Trained Random Forest model
│   ├── decision_tree_model.joblib  # Trained Decision Tree model
│   ├── xgboost_model.joblib        # Trained XGBoost model
│   ├── logistic_metadata.json      # Logistic Regression model info
│   ├── random_forest_metadata.json # Random Forest model info
│   ├── decision_tree_metadata.json # Decision Tree model info
│   └── xgboost_metadata.json       # XGBoost model info
│
├── scripts/
│   ├── generate_data.py            # Data generation script
│   ├── clean_preprocess_data.py    # Data cleaning and preprocessing
│   ├── eda_analysis.py             # Exploratory Data Analysis
│   ├── model_comparison.py         # Model training and comparison
│   ├── train_logistic_model.py     # Logistic Regression training
│   ├── train_random_forest_model.py # Random Forest training
│   ├── train_decision_tree_model.py # Decision Tree training
│   └── Train_XGBoost_model.py      # XGBoost training
│
├── outputs/
│   └── eda_plots/                  # Generated EDA plots (18 visualizations)
│
├── .venv/                          # Python virtual environment
├── README.md                       # This file
└── requirements.txt                # Python dependencies

```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment tool

### Step 1: Clone Repository
```bash
git clone https://github.com/hiralalparate385-netizen/faculty-risk-prediction.git
cd faculty-risk-prediction
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install streamlit plotly pandas numpy scikit-learn xgboost joblib streamlit-option-menu
```

### Step 4: Run the Application
```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

---

## 📖 Usage Guide

### 🏠 Dashboard Tab
1. **View Key Metrics** - See total faculty, risk distribution, and statistics
2. **Risk Distribution** - Visual pie chart showing low vs high risk faculty
3. **Key Insights** - Comparative statistics and trends

### 📊 Analytics Tab
Contains 4 sub-tabs for detailed analysis:

#### 📊 Features Tab
- Select any feature to visualize its distribution
- Compare distributions between high and low-risk faculty
- Interactive histogram and boxplot visualizations

#### 🔗 Correlations Tab
- Heatmap showing relationships between all features
- Identify which factors most correlate with risk

#### 📈 Trends Tab
- Multi-feature comparison
- See how different combinations affect risk
- Compare low vs high risk groups

#### 🎯 Risk Analysis Tab
- Analyze specific risk factors
- Student load impact
- Administrative roles impact

### 🔮 Prediction Tab
1. **Select Model** - Choose from 4 available models
2. **Input Faculty Details** - Use compact number inputs:
   - Courses Assigned (1-6)
   - Teaching Hours (0-30 hrs/week)
   - Total Students (10-300)
   - Admin Roles (0-5)
   - Years of Experience (1-40)
   - Preparation Hours (0-20 hrs/week)

3. **Compare with Averages** - See how inputs compare to dataset
4. **Click Predict** - Get instant risk assessment
5. **Review Results**:
   - Risk indicator (HIGH/LOW)
   - Risk score gauge
   - Detailed metrics (Risk probability, Workload index, Prep efficiency, Students/course)
   - Personalized recommendations
   - Similar faculty comparison
   - All models' predictions

### 📈 Model Comparison Tab
1. **View Performance Charts** - Compare metrics across models
2. **Detailed Metrics Table** - Accuracy, precision, recall, F1-score
3. **Model Details** - Select a model to see:
   - Model type
   - Training records
   - Features used
   - Why this model is useful
   - Advantages

### ℹ️ About Tab
- System overview and project information
- Key metrics explanation
- AI models used
- System statistics

---

## 🧠 How Predictions Work

### Risk Calculation
The system calculates risk using multiple factors:

```
Risk Score = f(
    courses_assigned,
    weekly_teaching_hours,
    total_students_handled,
    admin_roles_count,
    years_of_experience,
    preparation_hours_per_week,
    term,
    exam_type
)
```

### Workload Index
```
Workload Index = (courses × 15) + (hours × 2) + (students ÷ 20) + (prep_hours × 3)
```

### Efficiency Score
```
Efficiency = (prep_hours ÷ teaching_hours) × 100
```

### Risk Factors Identified
- 🔴 High course load (5+ courses)
- 🔴 High teaching hours (20+ hrs/week)
- 🟡 Large student population (200+ students)
- 🟡 Multiple admin roles (3+ roles)
- 🟠 Low preparation time

---

## 📊 Dashboard Features

### Performance & Aesthetics
- ✅ **Dark Theme** - Gradient backgrounds with modern color scheme
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile
- ✅ **Interactive Charts** - Hover for details, zoom, pan capabilities
- ✅ **Fast Loading** - Cached data and models for instant interactions
- ✅ **Professional UI** - Clean, organized, and user-friendly

### Color Scheme
- 🔴 **Primary Red** (#FF6B6B) - High risk, alerts
- 🔵 **Teal** (#4ECDC4) - Low risk, positive indicators
- 🟡 **Yellow** (#FFD93D) - Warnings, metrics highlighting
- ⚫ **Dark Background** (#0F1419) - Base dark theme

---

## 🔍 Key Insights from Data

### High-Risk vs Low-Risk Faculty
| Metric | High Risk | Low Risk | Difference |
|--------|-----------|----------|-----------|
| Avg Courses | 4.1 | 2.8 | +1.3 |
| Avg Teaching Hrs | 19.2 | 11.8 | +7.4 |
| Avg Students | 162 | 89 | +73 |
| Avg Prep Hours | 4.2 | 6.1 | -1.9 |

### Key Findings
1. **Course Load** - Most critical factor. Faculty with 5+ courses are at high risk
2. **Teaching Hours** - Teaching 20+ hours/week significantly increases risk
3. **Student Count** - Handling 200+ students correlates with higher risk
4. **Experience Level** - Senior faculty (10+ years) tend to have lower risk
5. **Preparation Time** - Adequate prep time (6+ hours) helps mitigate risk

---

## 🎯 Recommendations for Institutions

### For Faculty at Risk:
1. **Reduce Course Load** - Aim for 3-4 courses per semester
2. **Cap Teaching Hours** - Target 12-15 hours/week
3. **Distribute Students** - Break large classes into smaller sections
4. **Delegate Admin Work** - Reduce administrative responsibilities
5. **Increase Prep Time** - Allocate sufficient time for preparation and grading

### For Department Heads:
1. **Regular Monitoring** - Use FacultyAI to track workload changes
2. **Proactive Intervention** - Address high-risk indicators early
3. **Fair Resource Allocation** - Distribute courses and students equitably
4. **Support Systems** - Provide mentoring and professional development
5. **Work-Life Balance** - Foster sustainable workload culture

---

## 📈 Results & Performance

### System Accuracy
- **Best Model**: XGBoost (87.5% accuracy)
- **Most Balanced**: Random Forest (88% accuracy, 1.0 precision, 0.64 recall)
- **Most Interpretable**: Decision Tree (Clear decision pathways)

### Prediction Confidence
- The system provides confidence scores for each prediction
- Multiple model voting ensures robust predictions
- Consensus across models indicates high reliability

---

## 🔄 Data Pipeline

```
Raw Data Generation
        ↓
Data Cleaning & Preprocessing
        ↓
Feature Engineering
        ↓
Train-Test Split (80-20)
        ↓
Model Training (4 models)
        ↓
Model Evaluation & Comparison
        ↓
Deployment in Streamlit App
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"
```bash
# Solution: Install missing packages
pip install -r requirements.txt
```

### Issue: "Database not found"
```bash
# Solution: Ensure faculty.db is in the data/ directory
# If missing, run the generate_data script
python scripts/generate_data.py
```

### Issue: Model loading error
```bash
# Solution: Ensure all model files are in models/ directory
# Check that .joblib files exist
ls models/*.joblib
```

### Issue: Streamlit not responding
```bash
# Solution: Clear cache and restart
# Delete .streamlit folder
rm -rf .streamlit/
streamlit run app.py
```

---

## 📚 Learning Resources

### About the Models:
- **Logistic Regression**: Fast linear classifier
- **Random Forest**: Powerful ensemble method
- **Decision Trees**: Simple yet effective rules-based approach
- **XGBoost**: State-of-the-art gradient boosting

### References:
- [Scikit-Learn Documentation](https://scikit-learn.org)
- [XGBoost Documentation](https://xgboost.readthedocs.io)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Documentation](https://plotly.com/python)

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 Authors & Credits

- **Developer**: Roominesh
- **Project Type**: Hackathon Project #3
- **Date**: March 2026
- **License**: MIT

---

## 📧 Contact & Support

For issues, questions, or suggestions:
- GitHub Issues: [Create an issue](https://github.com/hiralalparate385-netizen/faculty-risk-prediction/issues)
- Email: Contact via GitHub profile

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Faculty of Educational Institutions for dataset insights
- The open-source community for amazing libraries
- Streamlit for making data applications accessible
- All contributors and users of this system

---

## 📌 Quick Links

- 🌐 **GitHub Repository**: [faculty-risk-prediction](https://github.com/hiralalparate385-netizen/faculty-risk-prediction)
- 📊 **Live Dashboard**: Run with `streamlit run app.py`
- 📖 **Documentation**: See this README
- 🎯 **Issues**: Report bugs and suggest features

---

**Last Updated**: March 18, 2026  
**Version**: 1.0.0  
**Status**: ✅ Production Ready

---

**Made with ❤️ for sustainable faculty workload management**
