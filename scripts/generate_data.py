"""
Data Generation Script for Faculty Workload Risk Prediction System
+ Data Drift Detection Integrated
"""

import sqlite3
import numpy as np
import pandas as pd
from pathlib import Path
import json

# Configuration
DATABASE_PATH = Path(__file__).parent.parent / "data" / "faculty.db"
RANDOM_SEED = 42
NUM_FACULTY = 120

TERMS = ["Independence", "Festival", "Republic", "Colors"]
EXAM_TYPES = ["Unit Test 1", "Mid Term", "Unit Test 2", "End Term"]


# =========================
# DATABASE SETUP
# =========================
def setup_database():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS faculty_workload_raw")
    
    cursor.execute("""
        CREATE TABLE faculty_workload_raw (
            faculty_id INTEGER PRIMARY KEY,
            courses_assigned INTEGER,
            weekly_teaching_hours INTEGER,
            total_students_handled INTEGER,
            admin_roles_count INTEGER,
            years_of_experience INTEGER,
            preparation_hours_per_week INTEGER,
            term TEXT,
            exam_type TEXT,
            workload_risk INTEGER
        )
    """)
    
    conn.commit()
    return conn


# =========================
# DATA GENERATION
# =========================
def generate_synthetic_data():
    np.random.seed(RANDOM_SEED)
    data = []
    
    for faculty_id in range(1, NUM_FACULTY + 1):
        
        experience = np.random.choice(
            np.concatenate([
                np.random.normal(15, 8, int(0.8 * NUM_FACULTY)),
                np.random.uniform(1, 5, int(0.2 * NUM_FACULTY))
            ])
        )
        experience = max(1, int(np.clip(experience, 1, 40)))
        
        courses = int(np.random.gamma(shape=2, scale=1.5) + 1)
        courses = np.clip(courses, 2, 5)
        
        weekly_hours = int(np.random.normal(13, 3))
        weekly_hours = max(6, min(weekly_hours, 24))
        
        total_students = int(np.random.lognormal(mean=3.5, sigma=0.7))
        total_students = max(10, min(total_students, 300))
        
        admin_roles = int(np.random.poisson(0.8))
        admin_roles = min(admin_roles, 3)
        
        if np.random.random() > 0.2:
            prep_hours = int(np.random.gamma(shape=3, scale=2))
            prep_hours = max(1, min(prep_hours, 20))
        else:
            prep_hours = None
        
        term = np.random.choice(TERMS)
        exam_type = np.random.choice(EXAM_TYPES)
        
        risk_score = (
            0.3 * (courses / 5) +
            0.25 * (weekly_hours / 24) +
            0.25 * (total_students / 200) +
            0.15 * (admin_roles / 3) +
            0.05 * (1 - experience / 40)
        )
        
        risk_score += np.random.normal(0, 0.1)
        workload_risk = 1 if risk_score > 0.55 else 0
        
        data.append({
            'faculty_id': faculty_id,
            'courses_assigned': courses,
            'weekly_teaching_hours': weekly_hours,
            'total_students_handled': total_students,
            'admin_roles_count': admin_roles,
            'years_of_experience': experience,
            'preparation_hours_per_week': prep_hours,
            'term': term,
            'exam_type': exam_type,
            'workload_risk': workload_risk
        })
    
    return pd.DataFrame(data)


# =========================
# INSERT DATA
# =========================
def insert_data_to_db(conn, df):
    cursor = conn.cursor()
    
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO faculty_workload_raw 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, tuple(row))
    
    conn.commit()


# =========================
# METADATA LOGGING
# =========================
def log_metadata(df):
    metadata = {
        'generation_timestamp': pd.Timestamp.now().isoformat(),
        'total_records': len(df),
        'columns': list(df.columns),
        'missing_values': df.isnull().sum().to_dict(),
        'risk_distribution': df['workload_risk'].value_counts().to_dict()
    }
    
    metadata_path = DATABASE_PATH.parent / "generation_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("Metadata saved to:", metadata_path)


# =========================
# DATA DRIFT DETECTION
# =========================
def detect_data_drift(df, threshold=0.2):
    baseline_path = DATABASE_PATH.parent / "baseline_stats.json"
    drift_report_path = DATABASE_PATH.parent / "drift_report.json"
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    current_stats = {}
    for col in numeric_cols:
        current_stats[col] = {
            "mean": float(df[col].mean()),
            "std": float(df[col].std())
        }
    
    # First run → create baseline
    if not baseline_path.exists():
        with open(baseline_path, "w") as f:
            json.dump(current_stats, f, indent=2)
        print("[INFO] Baseline created. No drift detection this run.")
        return False
    
    # Load baseline
    with open(baseline_path, "r") as f:
        baseline_stats = json.load(f)
    
    drift_detected = False
    drift_details = {}
    
    for col in numeric_cols:
        if col in baseline_stats:
            old_mean = baseline_stats[col]["mean"]
            new_mean = current_stats[col]["mean"]
            
            change = abs(new_mean - old_mean) / abs(old_mean) if old_mean != 0 else abs(new_mean)
            
            drift_details[col] = {
                "old_mean": old_mean,
                "new_mean": new_mean,
                "relative_change": change
            }
            
            if change > threshold:
                drift_detected = True
    
    # Save report
    with open(drift_report_path, "w") as f:
        json.dump({
            "timestamp": pd.Timestamp.now().isoformat(),
            "drift_detected": drift_detected,
            "details": drift_details
        }, f, indent=2)
    
    print("Drift report saved:", drift_report_path)
    
    # Update baseline
    with open(baseline_path, "w") as f:
        json.dump(current_stats, f, indent=2)
    
    return drift_detected


# =========================
# MAIN PIPELINE
# =========================
def main():
    print("=" * 60)
    print("Faculty Workload Data Generation + Drift Detection")
    print("=" * 60)
    
    print("\nSetting up database...")
    conn = setup_database()
    
    print("\nGenerating data...")
    df = generate_synthetic_data()
    
    print("\nInserting data...")
    insert_data_to_db(conn, df)
    conn.close()
    
    print("\nLogging metadata...")
    log_metadata(df)
    
    print("\nChecking data drift...")
    drift_flag = detect_data_drift(df)
    
    if drift_flag:
        print("[ALERT] Data drift detected! Trigger retraining.")
        # 👉 integrate your retraining script here
    else:
        print("[OK] No significant drift detected.")
    
    print("\nPipeline completed successfully!")


if __name__ == "__main__":
    main()