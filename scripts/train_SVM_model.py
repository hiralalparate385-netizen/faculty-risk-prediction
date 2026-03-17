import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
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
    # Scaling is CRITICAL for SVM
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    model = SVC(kernel='rbf', probability=True, random_state=42, class_weight='balanced')

    model.fit(X_train_scaled, y_train)
    return model, scaler

def evaluate_model(model, scaler, X_test, y_test, set_name="Test"):
    X_test_scaled = scaler.transform(X_test)
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

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

def save_model(model, scaler, feature_cols, train_metrics, test_metrics, X_train):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    model_path = MODELS_DIR / "svm_model.joblib"
    scaler_path = MODELS_DIR / "svm_scaler.joblib"

    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)

    print(f"\n[OK] Model saved: {model_path}")
    print(f"[OK] Scaler saved: {scaler_path}")

    metadata = {
        'model_type': 'SVM (SVC)',
        'model_path': str(model_path),
        'scaler_path': str(scaler_path),
        'training_timestamp': datetime.now().isoformat(),
        'training_records': len(X_train),
        'feature_names': feature_cols,
        'num_features': len(feature_cols),
        'model_parameters': {
            'kernel': 'rbf',
            'C': 1.0,
            'gamma': 'scale'
        },
        'justification': {
            'reason': 'Non-linear classification capability',
            'advantages': [
                'Effective in high-dimensional spaces',
                'Handles non-linear boundaries',
                'Robust with small datasets',
                'Works well with clear margin separation'
            ]
        },
        'training_metrics': train_metrics,
        'test_metrics': test_metrics
    }

    metadata_path = MODELS_DIR / "svm_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"[OK] Metadata saved: {metadata_path}")

    return metadata

def main():
    print("=" * 60)
    print("SVM Model Training")
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

    print("\nTraining SVM model...")
    model, scaler = train_model(X_train, y_train)
    print("[OK] Model trained successfully")

    print("\nTRAINING SET EVALUATION")
    train_metrics = evaluate_model(model, scaler, X_train, y_train, set_name="Train")

    print("\nTEST SET EVALUATION")
    test_metrics = evaluate_model(model, scaler, X_test, y_test, set_name="Test")

    print("\nSAVING MODEL")
    metadata = save_model(model, scaler, feature_cols, train_metrics, test_metrics, X_train)

    print("\n" + "=" * 60)
    print("Model Training Summary")
    print("=" * 60)
    print(f"Model Type: {metadata['model_type']}")
    print(f"Features: {metadata['num_features']}")
    print(f"Training Records: {metadata['training_records']}")
    print(f"Test Accuracy: {test_metrics['accuracy']:.4f}")
    print(f"Test F1-Score: {test_metrics['f1_score']:.4f}")
    print("\nSVM training complete! [OK]")

if __name__ == "__main__":
    main()