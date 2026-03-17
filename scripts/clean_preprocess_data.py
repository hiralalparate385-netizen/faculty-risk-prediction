"""
Data Cleaning and Preprocessing Script

This script reads raw faculty workload data from the database,
applies cleaning operations, and stores the cleaned data in a new table.

Operations:
- Duplicate removal
- Missing value imputation (median for numeric, mode for categorical)
- Outlier detection and capping (IQR method)
- Data validation and range checks
- Categorical encoding
"""

import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
import json

DATABASE_PATH = Path(__file__).parent.parent / "data" / "faculty.db"

def load_raw_data():
    """Load raw data from database."""
    conn = sqlite3.connect(DATABASE_PATH)
    query = "SELECT * FROM faculty_workload_raw"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def remove_duplicates(df):
    """Remove duplicate rows."""
    initial_count = len(df)
    df = df.drop_duplicates(subset=['faculty_id'])
    removed_count = initial_count - len(df)
    print(f"  - Duplicates removed: {removed_count}")
    return df

def handle_missing_values(df):
    """Handle missing values using median/mode imputation."""
    numeric_cols = [
        'courses_assigned', 'weekly_teaching_hours', 'total_students_handled',
        'admin_roles_count', 'years_of_experience', 'preparation_hours_per_week'
    ]
    categorical_cols = ['term', 'exam_type']
    
    missing_info = {}
    
    # Median imputation for numeric columns
    for col in numeric_cols:
        if df[col].isnull().any():
            missing_count = df[col].isnull().sum()
            median_val = df[col].median()
            df[col].fillna(median_val, inplace=True)
            missing_info[col] = missing_count
            print(f"  - {col}: {missing_count} missing values filled with median ({median_val})")
    
    # Mode imputation for categorical columns
    for col in categorical_cols:
        if df[col].isnull().any():
            missing_count = df[col].isnull().sum()
            mode_val = df[col].mode()[0]
            df[col].fillna(mode_val, inplace=True)
            missing_info[col] = missing_count
            print(f"  - {col}: {missing_count} missing values filled with mode ({mode_val})")
    
    return df, missing_info

def handle_outliers(df):
    """Handle outliers using IQR capping method."""
    numeric_cols = [
        'courses_assigned', 'weekly_teaching_hours', 'total_students_handled',
        'admin_roles_count', 'years_of_experience', 'preparation_hours_per_week'
    ]
    
    outlier_info = {}
    
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers_count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
        
        if outliers_count > 0:
            df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
            outlier_info[col] = outliers_count
            print(f"  - {col}: {outliers_count} outliers capped (bounds: [{lower_bound:.1f}, {upper_bound:.1f}])")
    
    return df, outlier_info

def validate_ranges(df):
    """Validate that numeric values fall within reasonable ranges."""
    validation_issues = []
    
    # Check ranges
    if (df['courses_assigned'] < 1).any() or (df['courses_assigned'] > 10).any():
        validation_issues.append("courses_assigned out of bounds [1, 10]")
    
    if (df['weekly_teaching_hours'] < 0).any() or (df['weekly_teaching_hours'] > 30).any():
        validation_issues.append("weekly_teaching_hours out of bounds [0, 30]")
    
    if (df['total_students_handled'] < 0).any():
        validation_issues.append("total_students_handled has negative values")
    
    if (df['admin_roles_count'] < 0).any() or (df['admin_roles_count'] > 5).any():
        validation_issues.append("admin_roles_count out of bounds [0, 5]")
    
    if (df['years_of_experience'] < 0).any() or (df['years_of_experience'] > 50).any():
        validation_issues.append("years_of_experience out of bounds [0, 50]")
    
    if validation_issues:
        print("  [WARNING] Validation issues found:")
        for issue in validation_issues:
            print(f"    - {issue}")
    else:
        print("  [OK] All numeric ranges validated")
    
    return df

def encode_categorical_variables(df):
    """Encode categorical variables for modeling."""
    # Create a copy with encoded columns
    df_encoded = df.copy()
    
    # One-hot encode 'term'
    term_dummies = pd.get_dummies(df['term'], prefix='term', drop_first=False)
    
    # One-hot encode 'exam_type'
    exam_dummies = pd.get_dummies(df['exam_type'], prefix='exam', drop_first=False)
    
    # Store original categorical columns for reference
    df_encoded['term_original'] = df['term']
    df_encoded['exam_type_original'] = df['exam_type']
    
    # Add encoded columns
    df_encoded = pd.concat([df_encoded, term_dummies, exam_dummies], axis=1)
    
    print(f"  [OK] Encoded {len(term_dummies.columns)} term categories")
    print(f"  [OK] Encoded {len(exam_dummies.columns)} exam categories")
    
    return df_encoded

def save_cleaned_data(conn, df):
    """Save cleaned data to database."""
    cursor = conn.cursor()
    
    # Drop existing cleaned table
    cursor.execute("DROP TABLE IF EXISTS faculty_workload_cleaned")
    
    # Save cleaned data to new table
    df.to_sql('faculty_workload_cleaned', conn, if_exists='replace', index=False)
    
    conn.commit()
    print(f"  [OK] Cleaned data saved to 'faculty_workload_cleaned' table ({len(df)} rows)")

def log_cleaning_report(df_raw, df_cleaned, missing_info, outlier_info):
    """Create a detailed cleaning report."""
    report = {
        'timestamp': pd.Timestamp.now().isoformat(),
        'raw_records': len(df_raw),
        'cleaned_records': len(df_cleaned),
        'duplicates_removed': len(df_raw) - len(df_cleaned),
        'missing_values_handled': {k: int(v) for k, v in missing_info.items()},
        'outliers_capped': {k: int(v) for k, v in outlier_info.items()},
        'columns_in_cleaned_data': list(df_cleaned.columns)
    }
    
    report_path = DATABASE_PATH.parent / "cleaning_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nCleaning report saved: {report_path}")
    return report

def main():
    """Main execution function."""
    print("=" * 60)
    print("Data Cleaning and Preprocessing")
    print("=" * 60)
    
    # Load raw data
    print("\nLoading raw data from database...")
    df_raw = load_raw_data()
    print(f"[OK] Loaded {len(df_raw)} records from 'faculty_workload_raw'")
    
    # Create a copy for cleaning
    df = df_raw.copy()
    
    # Remove duplicates
    print("\nRemoving duplicates...")
    df = remove_duplicates(df)
    
    # Handle missing values
    print("\nHandling missing values...")
    df, missing_info = handle_missing_values(df)
    
    # Handle outliers
    print("\nHandling outliers...")
    df, outlier_info = handle_outliers(df)
    
    # Validate ranges
    print("\nValidating numeric ranges...")
    df = validate_ranges(df)
    
    # Encode categorical variables
    print("\nEncoding categorical variables...")
    df_encoded = encode_categorical_variables(df)
    
    # Save cleaned data to database
    print("\nSaving cleaned data...")
    conn = sqlite3.connect(DATABASE_PATH)
    save_cleaned_data(conn, df_encoded)
    conn.close()
    
    # Generate report
    print("\nGenerating cleaning report...")
    report = log_cleaning_report(df_raw, df_encoded, missing_info, outlier_info)
    
    # Summary
    print("\n" + "=" * 60)
    print("Cleaning Summary")
    print("=" * 60)
    print(f"Raw records: {len(df_raw)}")
    print(f"Cleaned records: {len(df_encoded)}")
    print(f"Final dataset shape: {df_encoded.shape}")
    print(f"Risk distribution:\n{df_encoded['workload_risk'].value_counts().to_string()}")
    print("\nData cleaning complete! [OK]")

if __name__ == "__main__":
    main()
