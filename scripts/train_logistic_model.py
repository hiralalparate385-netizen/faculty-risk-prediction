import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib

DATABASE_PATH = Path(__file__).parent.parent / "data" / "faculty.db"
MODELS_DIR = Path(__file__).parent.parent / "models"

def load_cleaned_data():
    """Load cleaned data from database."""
    conn = sqlite3.connect(DATABASE_PATH)
    query = "SELECT * FROM faculty_workload_cleaned"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def prepare_features(df):
    """Prepare feature matrix and target vector."""
    
    # Identify feature columns (exclude target, identifier, and original categorical columns)
    exclude_cols = {'faculty_id', 'workload_risk', 'term_original', 'exam_type_original', 'term', 'exam_type'}
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    
    X = df[feature_cols].copy()
    y = df['workload_risk'].copy()
    
    print(f"Features selected: {len(feature_cols)}")
    print(f"  {', '.join(feature_cols[:3])}... (showing first 3)")
    
    return X, y, feature_cols

def train_model(X_train, y_train):
    """Train logistic regression model with hyperparameter tuning."""
    
    # Standardize features (important for logistic regression)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Train logistic regression
    model = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
    
    model.fit(X_train_scaled, y_train)
    
    return model, scaler

def evaluate_model(model, scaler, X_test, y_test, set_name="Test"):
    """Evaluate model performance."""
    
    X_test_scaled = scaler.transform(X_test)
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    # Confusion matrix
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
    
    return metrics, y_pred

def save_model(model, scaler, feature_cols, train_metrics, test_metrics, X_train):
    """Save model and metadata to disk."""
    
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save model
    model_path = MODELS_DIR / "logistic_model.joblib"
    joblib.dump(model, model_path)
    print(f"\n[OK] Model saved: {model_path}")
    
    # Save scaler
    scaler_path = MODELS_DIR / "logistic_scaler.joblib"
    joblib.dump(scaler, scaler_path)
    print(f"[OK] Scaler saved: {scaler_path}")
    
    # Create metadata
    metadata = {
        'model_type': 'LogisticRegression',
        'model_path': str(model_path),
        'scaler_path': str(scaler_path),
        'training_timestamp': datetime.now().isoformat(),
        'training_records': len(X_train),
        'feature_names': feature_cols,
        'num_features': len(feature_cols),
        'model_parameters': {
            'random_state': 42,
            'max_iter': 1000,
            'solver': 'lbfgs'
        },
        'justification': {
            'reason': 'Binary classification on small dataset',
            'advantages': [
                'High interpretability',
                'Feature coefficients show importance',
                'Stable on small datasets',
                'Linear decision boundary'
            ]
        },
        'training_metrics': train_metrics,
        'test_metrics': test_metrics,
        'feature_coefficients': {
            name: float(coef) for name, coef in zip(feature_cols, model.coef_[0])
        }
    }
    
    metadata_path = MODELS_DIR / "model_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"[OK] Metadata saved: {metadata_path}")
    
    return metadata

def main():
    """Main execution function."""
    print("=" * 60)
    print("Logistic Regression Model Training")
    print("=" * 60)
    
    # Load data
    print("\nLoading cleaned data...")
    df = load_cleaned_data()
    print(f"[OK] Loaded {len(df)} records")
    
    # Prepare features
    print("\nPreparing features...")
    X, y, feature_cols = prepare_features(df)
    
    # Train-test split (80-20)
    print("\nSplitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"  Train set: {len(X_train)} records")
    print(f"  Test set: {len(X_test)} records")
    print(f"  Class distribution (train): {y_train.value_counts().to_dict()}")
    print(f"  Class distribution (test): {y_test.value_counts().to_dict()}")
    
    # Train model
    print("\nTraining Logistic Regression model...")
    model, scaler = train_model(X_train, y_train)
    print("[OK] Model trained successfully")
    
    # Evaluate on training set
    print("\n" + "-" * 60)
    print("TRAINING SET EVALUATION")
    print("-" * 60)
    train_metrics, _ = evaluate_model(model, scaler, X_train, y_train, set_name="Train")
    
    # Evaluate on test set
    print("\n" + "-" * 60)
    print("TEST SET EVALUATION")
    print("-" * 60)
    test_metrics, y_pred = evaluate_model(model, scaler, X_test, y_test, set_name="Test")
    
    # Save model
    print("\n" + "-" * 60)
    print("SAVING MODEL")
    print("-" * 60)
    metadata = save_model(model, scaler, feature_cols, train_metrics, test_metrics, X_train)
    
    # Summary
    print("\n" + "=" * 60)
    print("Model Training Summary")
    print("=" * 60)
    print(f"Model Type: {metadata['model_type']}")
    print(f"Features: {metadata['num_features']}")
    print(f"Training Records: {metadata['training_records']}")
    print(f"Test Accuracy: {test_metrics['accuracy']:.4f}")
    print(f"Test F1-Score: {test_metrics['f1_score']:.4f}")
    print("\nModel training complete! [OK]")

if __name__ == "__main__":
    main()
