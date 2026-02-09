# 📊 Faculty Workload Intelligence System

An advanced machine learning-powered dashboard for predicting and analyzing faculty workload risk. This system helps academic institutions assess faculty workload distribution, identify at-risk faculty, and make data-driven decisions for resource allocation.

---

## 🎯 Project Overview

The Faculty Workload Intelligence System is a comprehensive solution designed to:
- **Predict workload risk** for individual faculty members using machine learning
- **Analyze patterns** in faculty workload distribution across the institution
- **Provide insights** about factors affecting faculty workload
- **Generate recommendations** for workload management and optimization

### Why This Matters
Faculty workload is a critical factor in:
- **Burnout prevention** - Identifying overworked faculty early
- **Retention** - Preventing loss of experienced educators
- **Quality education** - Ensuring faculty have time for effective teaching
- **Fairness** - Equitable distribution of responsibilities
- **Institutional health** - Maintaining a sustainable academic environment

---

## ✨ Key Features

### 1. **Real-Time Workload Prediction**
- Predict high/low workload risk for any faculty member
- Get instant probability scores and confidence metrics
- Interactive input with sliders and dropdowns
- Personalized recommendations based on profile

### 2. **Comprehensive Dashboard**
- **Single Prediction**: Detailed analysis for individual faculty
- **Dataset Analysis**: Patterns and statistics across all faculty
- **Model Insights**: Understand how predictions are made
- **About Section**: Documentation and usage guide

### 3. **Rich Visualizations**
- Risk distribution pie charts
- Workload component breakdowns
- Teaching load vs student load scatter plots
- Risk analysis by academic term and exam type
- Feature importance and coefficient charts
- Summary statistics and metrics

### 4. **Data-Driven Insights**
- Actionable recommendations for workload reduction
- Pattern analysis across different academic contexts
- Feature importance visualization
- Model transparency and explainability

### 5. **Easy-to-Use Interface**
- Streamlit-based web application
- Intuitive navigation with sidebar
- Multi-page design for different use cases
- Clean, professional dark-friendly styling

---

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Technical Stack](#technical-stack)
- [Detailed Usage](#detailed-usage)
- [Model Details](#model-details)
- [Database Schema](#database-schema)
- [File Descriptions](#file-descriptions)
- [How to Use Each Module](#how-to-use-each-module)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

---

## 💻 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Windows, macOS, or Linux
- Git (optional, for cloning)

### Step 1: Clone/Setup Project
```bash
# Navigate to project directory
cd Hackathon_3_Project
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

Or install packages individually:
```bash
pip install streamlit pandas numpy scikit-learn joblib matplotlib seaborn sqlite3
```

### Step 4: Verify Installation
```bash
python -c "import streamlit; import sklearn; print('✅ All packages installed successfully!')"
```

---

## 🚀 Quick Start

### 1. Generate Training Data
```bash
# Activate virtual environment first
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

# Run the data generation notebook
jupyter notebook scripts/generate_data.ipynb
# Or run in terminal:
python -m jupyter nbconvert --to notebook --execute scripts/generate_data.ipynb
```

This creates:
- `data/faculty.db` - SQLite database with 120 faculty records
- Table: `faculty_workload` with complete faculty metrics

### 2. Train the Model
```bash
# Run the model training notebook
jupyter notebook train_models.ipynb
# Or:
python -m jupyter nbconvert --to notebook --execute train_models.ipynb
```

This creates:
- `models/logistic_regression_model.joblib` - Trained ML model
- `models/scaler.joblib` - Feature scaler for preprocessing
- Performance metrics and model comparison results

### 3. Launch the Dashboard
```bash
# Make sure you're in the project root directory
# Windows: 
.venv\Scripts\python.exe -m streamlit run app.py

# macOS/Linux:
python -m streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

---

## 📁 Project Structure

```
Hackathon_3_Project/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── app.py                             # Main Streamlit application
├── data/
│   ├── faculty.db                     # SQLite database (generated)
│   └── [other data files]
├── models/
│   ├── logistic_regression_model.joblib  # Trained model (generated)
│   └── scaler.joblib                  # Feature scaler (generated)
├── scripts/
│   ├── generate_data.ipynb            # Data generation notebook
│   ├── train_models.ipynb             # Model training notebook (may exist)
│   └── eda_analysis.ipynb             # EDA notebook (may exist)
└── [other support files]
```

---

## 🛠️ Technical Stack

### Backend & ML
- **Scikit-Learn**: Machine learning (Logistic Regression)
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **SQLite**: Lightweight database

### Frontend
- **Streamlit**: Interactive web framework
- **Matplotlib & Seaborn**: Data visualization

### Utilities
- **Joblib**: Model serialization/deserialization

### Python Version
- Python 3.8+ (tested on 3.10, 3.11, 3.13)

---

## 🔍 Detailed Usage

### Dashboard Navigation

#### 📈 Single Prediction Page
**Purpose**: Predict workload risk for an individual faculty member

**Steps**:
1. Fill in the faculty profile:
   - **Teaching Load**: Courses, weekly hours, student count
   - **Admin & Development**: Administrative roles, experience, prep hours
   - **Academic Context**: Term and exam phase
2. Click "🚀 Analyze Workload Risk"
3. View results:
   - Risk status (HIGH/LOW)
   - Risk probability percentage
   - Confidence score
   - Workload component breakdown
   - Personalized recommendations
   - Risk explanation

**Output Includes**:
- ✅/⚠️ Risk status indicator
- 📊 Risk probability visualization (pie chart)
- 📈 Workload components breakdown (bar chart)
- 📋 Metrics summary table
- 💡 Actionable recommendations

#### 📊 Dataset Analysis Page
**Purpose**: Understand patterns in faculty workload distribution

**Displays**:
- Total faculty count and high/low risk split
- Average metrics across faculty
- Risk distribution visualization
- Teaching load vs student load relationship
- Risk patterns by academic term
- Risk patterns by exam type
- Comprehensive summary statistics

**Insights Gained**:
- Which terms have more high-risk faculty
- Relationship between teaching hours and risk
- Student load impact on workload
- Overall risk distribution

#### 🔬 Model Insights Page
**Purpose**: Understand how the ML model makes predictions

**Contains**:
- Model type and configuration details
- Feature list with impact descriptions
- Feature coefficients visualization (what increases/decreases risk)
- Model regularization and solver information
- Prediction threshold details
- Scaling methodology

**Key Info**:
- 🔴 Red bars = factors increasing risk
- 🟢 Green bars = factors decreasing risk
- Magnitude of bar = strength of influence

#### 📋 About Page
**Purpose**: Project documentation and reference

**Sections**:
- System overview and purpose
- Data sources and features
- Technology stack
- Feature descriptions
- Model details
- Usage instructions
- Important disclaimers
- Contact information

---

## 🤖 Model Details

### Algorithm: Logistic Regression
```
Classification Problem: Binary (High Risk / Low Risk)
Output: Probability between 0 and 1
Decision Threshold: 0.5
```

### Training Configuration
```
Framework: Scikit-Learn
Test Size: 25%
Training Samples: 90 (75% of 120)
Test Samples: 30 (25% of 120)
Random State: 42 (reproducible)
Regularization: L2 (Ridge) with C=1.0
Solver: lbfgs
Max Iterations: 1000
```

### Input Features (After Encoding)
1. **courses_assigned** - Number of courses taught (1-4)
2. **weekly_teaching_hours** - Hours spent teaching per week (5-25)
3. **preparation_hours_per_week** - Hours spent on preparation (5-30)
4. **total_students_handled** - Total students across all courses (30-300)
5. **admin_roles_count** - Administrative responsibilities (0-2)
6. **years_of_experience** - Years in academia (1-30)
7. **term_[encoded]** - Academic term (one-hot encoded)
8. **exam_type_[encoded]** - Exam phase (one-hot encoded)

### Output
```
0 = Low Workload Risk (probability < 0.5)
1 = High Workload Risk (probability >= 0.5)
Probability Score: Confidence in the prediction (0-100%)
```

### Model Performance Metrics
The model provides:
- **Accuracy**: Overall prediction correctness
- **Precision**: Of predicted high-risk, how many are correct
- **Recall**: Of actual high-risk, how many are detected
- **F1 Score**: Harmonic mean of precision and recall

---

## 📊 Database Schema

### Table: `faculty_workload`

| Column | Type | Description | Range |
|--------|------|-------------|-------|
| faculty_id | INTEGER | Unique identifier | 1-120 |
| courses_assigned | INTEGER | Number of courses | 1-4 |
| weekly_teaching_hours | INTEGER | Teaching hours per week | 5-25 |
| total_students_handled | INTEGER | Total students | 30-300 |
| admin_roles_count | INTEGER | Admin responsibilities | 0-2 |
| years_of_experience | INTEGER | Years in academia | 1-30 |
| preparation_hours_per_week | INTEGER | Prep hours per week | 5-30 |
| term | TEXT | Academic term | Independence/Festival/Republic/Colors |
| exam_type | TEXT | Exam phase | Unit Test 1/Mid/Unit Test 2/End |
| workload_risk | INTEGER | Target (0=Low, 1=High) | 0 or 1 |

### Sample Data
```
faculty_id=1, courses=2, weekly_hours=12, students=90, admin_roles=1, 
experience=8, prep_hours=12, term=Festival Term, exam=Unit Test 1, 
workload_risk=0
```

---

## 📄 File Descriptions

### Core Application
- **app.py**: Main Streamlit application with 4-page dashboard
  - Lines 1-35: Imports and configuration
  - Lines 37-60: Page setup and sidebar navigation
  - Lines 62-200: Single Prediction page logic
  - Lines 202-320: Dataset Analysis page logic
  - Lines 322-420: Model Insights page logic
  - Lines 422-500: About page information

### Data & Models
- **scripts/generate_data.ipynb**: 
  - Creates synthetic faculty dataset
  - Generates `data/faculty.db` SQLite database
  - Creates 120 realistic faculty records
  - Runs: ~5-10 seconds

- **train_models.ipynb** (Optional):
  - Loads data from database
  - Trains Logistic Regression model
  - Generates `models/logistic_regression_model.joblib`
  - Creates `models/scaler.joblib`
  - Outputs model performance metrics

### Data
- **data/faculty.db**: SQLite database containing faculty records
  - Single table: `faculty_workload`
  - 120 records with 10 columns each
  - Size: ~20-30 KB

### Models
- **models/logistic_regression_model.joblib**: Trained ML model
  - Joblib serialized Scikit-Learn LogisticRegression object
  - Size: ~2-5 KB
  - Contains learned coefficients and intercept

- **models/scaler.joblib**: Feature standardizer
  - Joblib serialized StandardScaler object
  - Contains mean and std deviation of features
  - Size: ~1-2 KB

---

## ⚙️ Configuration

### Streamlit Config (Optional)
Create `.streamlit/config.toml` for custom settings:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = true

[logger]
level = "info"
```

### Database Path Configuration
Located in `app.py` (lines ~30-35):
```python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "faculty.db")
```

Modify if database is in different location.

---

## 🐛 Troubleshooting

### Issue 1: "Module not found" errors
```
Solution:
1. Ensure virtual environment is activated
2. Run: pip install -r requirements.txt
3. Restart the Streamlit app
```

### Issue 2: Database not found error
```
Error: sqlite3.OperationalError: no such table: faculty_workload

Solution:
1. Run scripts/generate_data.ipynb first
2. Verify data/faculty.db was created
3. Check that you're running from project root directory
```

### Issue 3: Model files not found
```
Error: FileNotFoundError: models/logistic_regression_model.joblib

Solution:
1. Run train_models.ipynb to generate model files
2. Verify models/ directory exists
3. Check file permissions
```

### Issue 4: Streamlit not launching
```
Error: streamlit: command not found

Windows Solution:
.venv\Scripts\python.exe -m streamlit run app.py

macOS/Linux Solution:
source .venv/bin/activate
streamlit run app.py
```

### Issue 5: Port 8501 already in use
```
Solution:
streamlit run app.py --server.port 8502
(or use any available port)
```

### Issue 6: Charts not displaying
```
Solution:
1. Refresh browser (Ctrl+R or Cmd+R)
2. Clear Streamlit cache: Delete .streamlit/ folder
3. Restart Streamlit app
4. Ensure matplotlib is installed: pip install matplotlib
```

---

## 🎯 Use Cases

### Use Case 1: Early Intervention
- Run single prediction for new faculty member
- Identify if workload setup creates risk
- Adjust course load before semester starts

### Use Case 2: Institutional Planning
- Use Dataset Analysis to see risk distribution
- Identify high-risk periods (specific terms/exams)
- Adjust scheduling accordingly

### Use Case 3: Resource Allocation
- Use Model Insights to understand risk factors
- Prioritize support for controllable factors
- Allocate teaching assistants based on predictions

### Use Case 4: Retention & Wellness
- Track predictions over semesters
- Identify at-risk faculty for intervention
- Monitor effectiveness of support programs

---

## 📈 Future Enhancements

### Short-term
1. **Regression model variant** - Predict actual workload score (not just high/low)
2. **Historical tracking** - Store predictions over time
3. **Batch processing** - Predict for entire department at once
4. **Export functionality** - Download reports as PDF/Excel

### Medium-term
1. **Advanced models** - Try Random Forest, Gradient Boosting
2. **Cross-validation analysis** - Detailed model evaluation
3. **Custom metrics** - Institution-specific risk factors
4. **Real data integration** - Use actual campus data

### Long-term
1. **Predictive scheduling** - Suggest optimal course assignments
2. **Impact analysis** - Show what-if scenarios
3. **Machine learning pipeline** - Automated retraining
4. **Mobile app** - Native iOS/Android application
5. **Multi-institution support** - Compare across universities

---

## 🤝 Contributing

### Reporting Issues
1. Describe the problem clearly
2. Include error messages and screenshots
3. List steps to reproduce
4. Share Python and package versions

### Suggesting Improvements
1. Check if suggestion already exists
2. Describe use case and benefits
3. Provide example/mockup if applicable
4. Suggest implementation approach

### Code Contributions
1. Fork the project
2. Create feature branch: `git checkout -b feature/YourFeature`
3. Commit changes: `git commit -m 'Add YourFeature'`
4. Push to branch: `git push origin feature/YourFeature`
5. Open Pull Request

---

## 📚 Learning Resources

### Machine Learning Concepts
- [Scikit-Learn Documentation](https://scikit-learn.org/)
- [Logistic Regression](https://en.wikipedia.org/wiki/Logistic_regression)
- [Feature Scaling](https://scikit-learn.org/stable/modules/preprocessing.html#standardization-or-mean-removal-and-variance-scaling)

### Streamlit Development
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit API Reference](https://docs.streamlit.io/library/api-reference)
- [Streamlit Examples](https://github.com/streamlit/streamlit/tree/develop/docs/static/demo_data)

### Python Data Science
- [Pandas Documentation](https://pandas.pydata.org/)
- [Matplotlib Tutorial](https://matplotlib.org/stable/tutorials/index.html)
- [NumPy Guide](https://numpy.org/doc/stable/)

---

## 📝 License

This project is provided as-is for educational and institutional use. 
For commercial use, please contact the development team.

---

## 👥 Team & Contact

**Project**: Faculty Workload Intelligence System  
**Version**: 1.0  
**Date**: February 2026  
**Status**: Production Ready ✅

### Credits
- Developed for Hackathon 3
- Data Science Team
- Machine Learning Research Group

### Support
For questions, issues, or feedback:
- Email: [project-email]
- Issues: [GitHub Issues Link]
- Documentation: See this README

---

## 📊 System Requirements

### Minimum
- Python 3.8+
- 2GB RAM
- 500MB Disk Space
- Modern web browser

### Recommended
- Python 3.10+
- 4GB+ RAM
- SSD (for faster operations)
- Chrome/Firefox/Safari/Edge (latest)

---

## ✅ Validation Checklist

- [x] Data generation successful
- [x] Model training completed
- [x] Streamlit app runs without errors
- [x] All pages load correctly
- [x] Visualizations display properly
- [x] Predictions work as expected
- [x] Database schema correct
- [x] Documentation complete

---

## 🎓 Educational Value

This project demonstrates:
- **ML Implementation**: Real-world machine learning workflow
- **Web Development**: Streamlit for rapid prototyping
- **Data Pipeline**: From data generation to model deployment
- **Data Visualization**: Creating insightful charts and graphs
- **Best Practices**: Clean code, documentation, error handling
- **Full Stack**: Database, backend, frontend integration

---

## 📋 FAQ

**Q: Can I use real faculty data?**  
A: Yes! Replace the synthetic data with actual faculty records. Ensure data privacy compliance.

**Q: How accurate is the model?**  
A: The model is trained on synthetic data. Real-world accuracy depends on actual data quality and patterns.

**Q: Can I customize the risk threshold?**  
A: Yes, modify the prediction threshold in the code (currently 0.5). Change it to `model.predict_proba(input_scaled)[0][1] >= 0.6` for stricter classification.

**Q: How often should I retrain the model?**  
A: Retrain when institutional patterns change (semesters, academic calendars) or with new data collection.

**Q: Can I add more features?**  
A: Yes, add new columns to the database and retrain the model. Update the input form in `app.py` accordingly.

**Q: Is the data encrypted?**  
A: Current implementation stores data plainly. Implement encryption for sensitive institutional data.

---

## 🚀 Getting Help

1. **Check this README** - Most questions are answered here
2. **Review error messages** - They usually indicate the exact problem
3. **Check logs** - Streamlit shows detailed error logs
4. **Consult documentation** - Linked throughout this file
5. **Contact development team** - For unresolved issues

---

## 📞 Version History

### v1.0 (Current)
- ✅ Initial release
- ✅ 4-page dashboard
- ✅ Single prediction engine
- ✅ Dataset analysis
- ✅ Model transparency features
- ✅ Comprehensive documentation

### Future Versions
- v1.1 - Enhanced visualizations
- v1.2 - Real data connectors
- v2.0 - Advanced ML models

---

**Last Updated**: February 2026  
**Status**: Production Ready ✅  
**Support Level**: Active Development

---

**Thank you for using the Faculty Workload Intelligence System! 📊**
