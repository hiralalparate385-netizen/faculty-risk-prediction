import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Paths
DATABASE_PATH = Path(__file__).parent.parent / "data" / "faculty.db"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "eda_plots"

# Create output folder
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sns.set(style="whitegrid")

def load_data():
    conn = sqlite3.connect(DATABASE_PATH)
    df = pd.read_sql_query("SELECT * FROM faculty_workload_cleaned", conn)
    conn.close()
    return df

def plot_target_distribution(df):
    plt.figure()
    sns.countplot(x='workload_risk', data=df)
    plt.title("Workload Risk Distribution")
    plt.xlabel("Risk (0 = Low, 1 = High)")
    plt.ylabel("Count")
    plt.savefig(OUTPUT_DIR / "target_distribution.png")
    plt.close()

def plot_numeric_distributions(df):
    numeric_cols = [
        'courses_assigned',
        'weekly_teaching_hours',
        'total_students_handled',
        'admin_roles_count',
        'years_of_experience',
        'preparation_hours_per_week'
    ]

    for col in numeric_cols:
        plt.figure()
        sns.histplot(df[col], kde=True)
        plt.title(f"Distribution of {col}")
        plt.savefig(OUTPUT_DIR / f"{col}_distribution.png")
        plt.close()

def plot_boxplots(df):
    numeric_cols = [
        'courses_assigned',
        'weekly_teaching_hours',
        'total_students_handled',
        'admin_roles_count',
        'years_of_experience',
        'preparation_hours_per_week'
    ]

    for col in numeric_cols:
        plt.figure()
        sns.boxplot(x='workload_risk', y=col, data=df)
        plt.title(f"{col} vs Workload Risk")
        plt.savefig(OUTPUT_DIR / f"{col}_vs_risk_boxplot.png")
        plt.close()

def plot_correlation_matrix(df):
    plt.figure(figsize=(10, 8))
    corr = df.corr(numeric_only=True)
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.savefig(OUTPUT_DIR / "correlation_matrix.png")
    plt.close()

def plot_categorical_analysis(df):
    # Term vs Risk
    plt.figure()
    sns.countplot(x='term_original', hue='workload_risk', data=df)
    plt.title("Term vs Workload Risk")
    plt.xticks(rotation=30)
    plt.savefig(OUTPUT_DIR / "term_vs_risk.png")
    plt.close()

    # Exam Type vs Risk
    plt.figure()
    sns.countplot(x='exam_type_original', hue='workload_risk', data=df)
    plt.title("Exam Type vs Workload Risk")
    plt.xticks(rotation=30)
    plt.savefig(OUTPUT_DIR / "exam_vs_risk.png")
    plt.close()

def plot_feature_importance_style(df):
    # Mean comparison
    grouped = df.groupby('workload_risk').mean(numeric_only=True).T

    grouped.plot(kind='bar', figsize=(12,6))
    plt.title("Feature Comparison (Low vs High Risk)")
    plt.ylabel("Mean Value")
    plt.xticks(rotation=45)
    plt.savefig(OUTPUT_DIR / "feature_comparison.png")
    plt.close()

def main():
    print("=" * 60)
    print("EDA ANALYSIS")
    print("=" * 60)

    df = load_data()
    print(f"Loaded {len(df)} records")

    print("\nGenerating plots...")

    plot_target_distribution(df)
    plot_numeric_distributions(df)
    plot_boxplots(df)
    plot_correlation_matrix(df)
    plot_categorical_analysis(df)
    plot_feature_importance_style(df)

    print(f"\n[OK] All plots saved in: {OUTPUT_DIR}")
    print("\nEDA complete! 🚀")

if __name__ == "__main__":
    main()