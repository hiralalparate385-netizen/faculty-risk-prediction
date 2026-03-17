import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

DATABASE_PATH = Path(__file__).parent.parent / "data" / "faculty.db"

# -------------------------------
# Load Data
# -------------------------------
def load_data():
    conn = sqlite3.connect(DATABASE_PATH)
    df = pd.read_sql_query("SELECT * FROM faculty_workload_cleaned", conn)
    conn.close()
    return df

# -------------------------------
# Prepare Features
# -------------------------------
def prepare_features(df):
    exclude_cols = {'faculty_id', 'workload_risk', 'term_original', 'exam_type_original', 'term', 'exam_type'}
    feature_cols = [col for col in df.columns if col not in exclude_cols]

    X = df[feature_cols]
    y = df['workload_risk']

    return X, y

# -------------------------------
# Evaluate Function
# -------------------------------
def evaluate(y_true, y_pred):
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1_score": f1_score(y_true, y_pred, zero_division=0)
    }

# -------------------------------
# Main
# -------------------------------
def main():
    print("="*60)
    print("MODEL COMPARISON")
    print("="*60)

    df = load_data()
    X, y = prepare_features(df)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    results = []

    # -------------------------------
    # 1. Logistic Regression
    # -------------------------------
    scaler_lr = StandardScaler()
    X_train_lr = scaler_lr.fit_transform(X_train)
    X_test_lr = scaler_lr.transform(X_test)

    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train_lr, y_train)

    y_pred = lr.predict(X_test_lr)
    metrics = evaluate(y_test, y_pred)
    results.append({"Model": "Logistic Regression", **metrics})

    # -------------------------------
    # 2. Decision Tree
    # -------------------------------
    dt = DecisionTreeClassifier(max_depth=5, random_state=42)
    dt.fit(X_train, y_train)

    y_pred = dt.predict(X_test)
    metrics = evaluate(y_test, y_pred)
    results.append({"Model": "Decision Tree", **metrics})

    # -------------------------------
    # 3. Random Forest
    # -------------------------------
    rf = RandomForestClassifier(n_estimators=100, max_depth=7, random_state=42)
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)
    metrics = evaluate(y_test, y_pred)
    results.append({"Model": "Random Forest", **metrics})

    # -------------------------------
    # 4. XGBoost
    # -------------------------------
    xgb = XGBClassifier(
        n_estimators=150,
        max_depth=5,
        learning_rate=0.1,
        eval_metric='logloss',
        use_label_encoder=False,
        random_state=42
    )
    xgb.fit(X_train, y_train)

    y_pred = xgb.predict(X_test)
    metrics = evaluate(y_test, y_pred)
    results.append({"Model": "XGBoost", **metrics})

    # -------------------------------
    # Results Table
    # -------------------------------
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(by="f1_score", ascending=False)

    print("\nModel Comparison Results:")
    print(results_df.to_string(index=False))

    print("\nBest Model Based on F1-Score:")
    print(results_df.iloc[0]["Model"])

    print("\nComparison complete! [OK]")

# -------------------------------
if __name__ == "__main__":
    main()