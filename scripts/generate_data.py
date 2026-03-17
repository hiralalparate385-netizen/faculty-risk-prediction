"""
Data Generation Script for Faculty Workload Risk Prediction System

This script generates realistic synthetic university faculty workload data
and stores it in a SQLite database. The data simulates a small college with
~100-150 faculty members with naturally imperfect characteristics.
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

# Academic terms and exam types
TERMS = ["Independence", "Festival", "Republic", "Colors"]
EXAM_TYPES = ["Unit Test 1", "Mid Term", "Unit Test 2", "End Term"]

def setup_database():
    """Create database and table if they don't exist."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Drop existing table for fresh generation
    cursor.execute("DROP TABLE IF EXISTS faculty_workload_raw")
    
    # Create table
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

def generate_synthetic_data():
    """Generate realistic synthetic faculty workload data."""
    
    np.random.seed(RANDOM_SEED)
    data = []
    
    for faculty_id in range(1, NUM_FACULTY + 1):
        # Years of experience: mostly 5-30, some 1-5
        experience = np.random.choice(
            np.concatenate([
                np.random.normal(15, 8, int(0.8 * NUM_FACULTY)),
                np.random.uniform(1, 5, int(0.2 * NUM_FACULTY))
            ])
        )
        experience = max(1, int(np.clip(experience, 1, 40)))
        
        # Courses assigned: 2-5 courses with skew toward higher
        courses = int(np.random.gamma(shape=2, scale=1.5) + 1)
        courses = np.clip(courses, 2, 5)
        
        # Weekly teaching hours: normally distributed around 12-15 hours
        weekly_hours = int(np.random.normal(13, 3))
        weekly_hours = max(6, min(weekly_hours, 24))
        
        # Total students: lognormal distribution (skewed toward larger classes)
        total_students = int(np.random.lognormal(mean=3.5, sigma=0.7))
        total_students = max(10, min(total_students, 300))
        
        # Admin roles: Poisson distribution
        admin_roles = int(np.random.poisson(0.8))
        admin_roles = min(admin_roles, 3)
        
        # Preparation hours: mostly present, some missing values (~20% missing)
        if np.random.random() > 0.2:
            prep_hours = int(np.random.gamma(shape=3, scale=2))
            prep_hours = max(1, min(prep_hours, 20))
        else:
            prep_hours = None  # Missing value
        
        # Select term and exam type (can vary by record)
        term = np.random.choice(TERMS)
        exam_type = np.random.choice(EXAM_TYPES)
        
        # Calculate workload risk based on weighted features
        # Higher courses, hours, students → higher risk
        risk_score = (
            0.3 * (courses / 5) +
            0.25 * (weekly_hours / 24) +
            0.25 * (total_students / 200) +
            0.15 * (admin_roles / 3) +
            0.05 * (1 - experience / 40)  # Junior faculty slightly higher risk
        )
        
        # Add some stochasticity (label noise) to make it realistic
        risk_score += np.random.normal(0, 0.1)
        
        # Threshold: faculty above 0.55 are at high risk
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

def insert_data_to_db(conn, df):
    """Insert generated data into database."""
    cursor = conn.cursor()
    
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO faculty_workload_raw 
            (faculty_id, courses_assigned, weekly_teaching_hours, 
             total_students_handled, admin_roles_count, years_of_experience,
             preparation_hours_per_week, term, exam_type, workload_risk)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row['faculty_id'],
            row['courses_assigned'],
            row['weekly_teaching_hours'],
            row['total_students_handled'],
            row['admin_roles_count'],
            row['years_of_experience'],
            row['preparation_hours_per_week'],
            row['term'],
            row['exam_type'],
            row['workload_risk']
        ))
    
    conn.commit()

def log_metadata(df):
    """Log metadata about generated data."""
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

def main():
    """Main execution function."""
    print("=" * 60)
    print("Faculty Workload Data Generation")
    print("=" * 60)
    
    # Setup database
    print("\nSetting up database...")
    conn = setup_database()
    print(f"[OK] Database created: {DATABASE_PATH}")
    
    # Generate data
    print("\nGenerating synthetic faculty data...")
    df = generate_synthetic_data()
    print(f"[OK] Generated {len(df)} faculty records")
    
    # Insert into database
    print("\nInserting data into database...")
    insert_data_to_db(conn, df)
    conn.close()
    print("[OK] Data inserted successfully")
    
    # Log metadata
    print("\nLogging metadata...")
    log_metadata(df)
    
    # Display summary
    print("\nData Summary:")
    print(f"  - Total Records: {len(df)}")
    print(f"  - High Risk (1): {(df['workload_risk'] == 1).sum()}")
    print(f"  - Low Risk (0): {(df['workload_risk'] == 0).sum()}")
    print(f"  - Missing Prep Hours: {df['preparation_hours_per_week'].isnull().sum()}")
    print(f"  - Date Range: {TERMS}")
    print(f"  - Exam Types: {EXAM_TYPES}")
    print("\nData generation complete! [OK]")

if __name__ == "__main__":
    main()
