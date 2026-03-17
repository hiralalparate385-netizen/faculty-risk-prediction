import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib

DATABASE_PATH = Path(__file__).parent.parent / "data" / "faculty.db"
MODELS_DIR = Path(__file__).parent.parent / "models"

def load_cleaned_data():
    conn = sqlite3.connect(DATABASE_PATH)
    query = "SELECT * FROM faculty_workload_cleaned"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def prepare_features(df):
    exclude_cols = {'faculty_id', 'workload_risk', 'term_original', 'exam_type_original', 'term', 'exam_type'}
    feature_cols = [col for col in df.columns if col not in exclude_cols]

    X = df[feature_cols].copy()
    y = df['workload_risk'].copy()

    print(f"Features selected: {len(feature_cols)}")
    print(f"  {', '.join(feature_cols[:3])}...")

    return X, y, feature_cols

def train_model(X_train, y_train):
    model = RandomForestClassifier(n_estimators=100, max_depth=7, random_state=42, class_weight='balanced')

    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test, set_name="Test"):
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    cm = confusion_matrix(y_test, y_pred)

    print(f"\n{set_name} Set Performance:")
    print(f"  Accuracy:  {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1-Score:  {f1:.4f}")

    print(f"\nConfusion Matrix ({set_name}):")
    print(f"  TN: {cm[0,0]}, FP: {cm[0,1]}")
    print(f"  FN: {cm[1,0]}, TP: {cm[1,1]}")

    print(f"\nClassification Report ({set_name}):")
    print(classification_report(y_test, y_pred, target_names=['Low Risk', 'High Risk']))

    metrics = {
        'accuracy': float(accuracy),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1),
        'confusion_matrix': {
            'tn': int(cm[0,0]),
            'fp': int(cm[0,1]),
            'fn': int(cm[1,0]),
            'tp': int(cm[1,1])
        }
    }

    return metrics

def save_model(model, feature_cols, train_metrics, test_metrics, X_train):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    model_path = MODELS_DIR / "random_forest_model.joblib"
    joblib.dump(model, model_path)
    print(f"\n[OK] Model saved: {model_path}")

    metadata = {
        'model_type': 'RandomForestClassifier',
        'model_path': str(model_path),
        'training_timestamp': datetime.now().isoformat(),
        'training_records': len(X_train),
        'feature_names': feature_cols,
        'num_features': len(feature_cols),
        'model_parameters': {
            'n_estimators': 100,
            'max_depth': 7,
            'min_samples_split': 5,
            'min_samples_leaf': 2,
            'random_state': 42
        },
        'justification': {
            'reason': 'Ensemble method for improved accuracy',
            'advantages': [
                'Reduces overfitting compared to single tree',
                'Captures non-linear relationships',
                'Handles feature interactions automatically',
                'Robust to noise'
            ]
        },
        'training_metrics': train_metrics,
        'test_metrics': test_metrics,
        'feature_importance': {
            name: float(imp) for name, imp in zip(feature_cols, model.feature_importances_)
        }
    }

    metadata_path = MODELS_DIR / "random_forest_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"[OK] Metadata saved: {metadata_path}")

    return metadata

def main():
    print("=" * 60)
    print("Random Forest Model Training")
    print("=" * 60)

    print("\nLoading cleaned data...")
    df = load_cleaned_data()
    print(f"[OK] Loaded {len(df)} records")

    print("\nPreparing features...")
    X, y, feature_cols = prepare_features(df)

    print("\nSplitting data (80-20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("\nTraining Random Forest model...")
    model = train_model(X_train, y_train)
    print("[OK] Model trained successfully")

    print("\nTRAINING SET EVALUATION")
    train_metrics = evaluate_model(model, X_train, y_train, set_name="Train")

    print("\nTEST SET EVALUATION")
    test_metrics = evaluate_model(model, X_test, y_test, set_name="Test")

    print("\nSAVING MODEL")
    metadata = save_model(model, feature_cols, train_metrics, test_metrics, X_train)

    print("\n" + "=" * 60)
    print("Model Training Summary")
    print("=" * 60)
    print(f"Model Type: {metadata['model_type']}")
    print(f"Features: {metadata['num_features']}")
    print(f"Training Records: {metadata['training_records']}")
    print(f"Test Accuracy: {test_metrics['accuracy']:.4f}")
    print(f"Test F1-Score: {test_metrics['f1_score']:.4f}")
    print("\nRandom Forest training complete! [OK]")

if __name__ == "__main__":
    main()