"""
Post-Mortem Analysis Module
Compares initial vs current model states and explains metric changes
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple, List
import pandas as pd
import numpy as np


class PostMortemAnalyzer:
    """Analyzes model performance changes over time as data grows"""
    
    def __init__(self, model_dir: Path, data_dir: Path):
        self.model_dir = model_dir
        self.data_dir = data_dir
        self.baseline_path = data_dir / "postmortem_baseline.json"
        self.history_path = data_dir / "postmortem_history.json"
        
    def load_current_metrics(self) -> Dict:
        """Load current metrics from all model metadata files"""
        metrics = {}
        
        for model_file in self.model_dir.glob("*_metadata.json"):
            with open(model_file) as f:
                metadata = json.load(f)
                model_name = model_file.stem.replace("_metadata", "")
                if model_name == "model":
                    model_name = "logistic"
                
                metrics[model_name] = {
                    "accuracy": metadata.get("test_metrics", {}).get("accuracy", 0),
                    "precision": metadata.get("test_metrics", {}).get("precision", 0),
                    "recall": metadata.get("test_metrics", {}).get("recall", 0),
                    "f1_score": metadata.get("test_metrics", {}).get("f1_score", 0),
                    "training_records": metadata.get("training_records", 0),
                    "timestamp": metadata.get("training_timestamp", ""),
                }
        
        # Handle backward compat for logistic model metadata
        main_metadata_path = self.model_dir / "model_metadata.json"
        if main_metadata_path.exists() and "logistic" not in metrics:
            with open(main_metadata_path) as f:
                metadata = json.load(f)
                metrics["logistic"] = {
                    "accuracy": metadata.get("test_metrics", {}).get("accuracy", 0),
                    "precision": metadata.get("test_metrics", {}).get("precision", 0),
                    "recall": metadata.get("test_metrics", {}).get("recall", 0),
                    "f1_score": metadata.get("test_metrics", {}).get("f1_score", 0),
                    "training_records": metadata.get("training_records", 0),
                    "timestamp": metadata.get("training_timestamp", ""),
                }
        
        return metrics
    
    def load_baseline_metrics(self) -> Dict:
        """Load baseline metrics from initialization"""
        if self.baseline_path.exists():
            with open(self.baseline_path) as f:
                return json.load(f)
        return None
    
    def initialize_baseline(self):
        """Create initial baseline snapshot (call once at startup)"""
        if not self.baseline_path.exists():
            current = self.load_current_metrics()
            baseline = {
                "timestamp": datetime.now().isoformat(),
                "metrics": current,
                "description": "Initial model baseline snapshot"
            }
            with open(self.baseline_path, 'w') as f:
                json.dump(baseline, f, indent=2)
            return baseline
        return self.load_baseline_metrics()
    
    def load_history(self) -> List[Dict]:
        """Load historical metrics snapshots"""
        if self.history_path.exists():
            with open(self.history_path) as f:
                return json.load(f)
        return []
    
    def add_history_snapshot(self):
        """Add current metrics to history"""
        history = self.load_history()
        current = self.load_current_metrics()
        
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "metrics": current
        }
        
        history.append(snapshot)
        
        with open(self.history_path, 'w') as f:
            json.dump(history, f, indent=2)
    
    def compare_metrics(self, baseline: Dict, current: Dict) -> Dict:
        """Compare baseline vs current metrics for all models"""
        comparison = {}
        
        for model_name in current.keys():
            baseline_m = baseline.get("metrics", {}).get(model_name, {})
            current_m = current[model_name]
            
            comparison[model_name] = {}
            
            for metric in ["accuracy", "precision", "recall", "f1_score"]:
                baseline_val = baseline_m.get(metric, 0)
                current_val = current_m.get(metric, 0)
                
                change = current_val - baseline_val
                pct_change = (change / baseline_val * 100) if baseline_val != 0 else 0
                
                comparison[model_name][metric] = {
                    "baseline": baseline_val,
                    "current": current_val,
                    "change": change,
                    "pct_change": pct_change,
                    "direction": "improved" if change > 0 else "degraded" if change < 0 else "same"
                }
            
            # Data growth
            baseline_records = baseline_m.get("training_records", 0)
            current_records = current_m.get("training_records", 0)
            comparison[model_name]["data_growth"] = {
                "baseline_records": baseline_records,
                "current_records": current_records,
                "growth": current_records - baseline_records,
                "growth_pct": (current_records / baseline_records * 100 - 100) if baseline_records > 0 else 0
            }
        
        return comparison
    
    def generate_insights(self, comparison: Dict, df: pd.DataFrame, baseline: Dict) -> Dict:
        """Generate insights explaining metric changes"""
        
        insights = {
            "overall_assessment": "",
            "data_quality": "",
            "model_specific": {},
            "recommendations": [],
            "key_factors": []
        }
        
        # Calculate baseline data stats
        baseline_records = list(baseline.get("metrics", {}).values())[0].get("training_records", 0)
        current_records = len(df)
        data_growth_pct = (current_records / baseline_records * 100 - 100) if baseline_records > 0 else 0
        
        # Overall assessment
        all_improved = all(
            all(comparison[m][metric]["direction"] == "improved" 
                for metric in ["accuracy", "precision", "recall", "f1_score"])
            for m in comparison
        )
        all_degraded = all(
            all(comparison[m][metric]["direction"] == "degraded" 
                for metric in ["accuracy", "precision", "recall", "f1_score"])
            for m in comparison
        )
        
        if all_improved:
            insights["overall_assessment"] = "📈 Excellent: All models show significant improvement across all metrics"
        elif all_degraded:
            insights["overall_assessment"] = "📉 Concerning: Models show degraded performance - data quality or distribution changes may be factors"
        else:
            insights["overall_assessment"] = "🔄 Mixed: Some models improved while others degraded - fine-tuning needed"
        
        # Data quality insights
        risk_distribution = df['workload_risk'].value_counts().to_dict()
        risk_ratio = risk_distribution.get(1, 0) / len(df) if len(df) > 0 else 0
        
        insights["data_quality"] = {
            "data_growth": f"Dataset grew by {data_growth_pct:.1f}% ({baseline_records} → {current_records} records)",
            "current_risk_ratio": f"{risk_ratio * 100:.1f}% high-risk faculty",
            "class_balance": "✅ Well-balanced" if 0.2 < risk_ratio < 0.5 else "⚠️ Skewed class distribution"
        }
        
        # Model-specific insights
        for model_name, metrics in comparison.items():
            model_insights = []
            
            accuracy_change = metrics["accuracy"]["change"]
            if accuracy_change > 0.05:
                model_insights.append(f"Accuracy improved by {accuracy_change*100:.2f}% - strong overall performance gain")
            elif accuracy_change < -0.05:
                model_insights.append(f"Accuracy declined by {abs(accuracy_change)*100:.2f}% - investigate data distribution changes")
            
            recall_change = metrics["recall"]["change"]
            if recall_change > 0.05:
                model_insights.append(f"Recall improved by {recall_change*100:.2f}% - better at detecting high-risk faculty")
            elif recall_change < -0.05:
                model_insights.append(f"Recall declined by {abs(recall_change)*100:.2f}% - missing more high-risk cases")
            
            precision_change = metrics["precision"]["change"]
            if precision_change > 0.05:
                model_insights.append(f"Precision improved by {precision_change*100:.2f}% - fewer false positives")
            elif precision_change < -0.05:
                model_insights.append(f"Precision declined by {abs(precision_change)*100:.2f}% - more false alarms")
            
            insights["model_specific"][model_name] = model_insights if model_insights else ["Metrics remain stable"]
        
        # Key factors explaining changes
        if data_growth_pct > 10:
            insights["key_factors"].append(f"📊 Significant data growth ({data_growth_pct:.1f}%) likely improved model generalization")
        
        # Check for data quality issues
        missing_prep_hours = (df['preparation_hours_per_week'].isna().sum() / len(df)) * 100 if len(df) > 0 else 0
        if missing_prep_hours > 5:
            insights["key_factors"].append(f"⚠️ {missing_prep_hours:.1f}% missing preparation hours data may affect predictions")
        
        # Feature variance
        student_ratio = df['total_students_handled'].std() / df['total_students_handled'].mean() if df['total_students_handled'].mean() > 0 else 0
        if student_ratio < 0.5:
            insights["key_factors"].append("📌 Low variance in student load - data may be homogeneous")
        elif student_ratio > 1.0:
            insights["key_factors"].append("📊 High variance in student load - diverse faculty profiles captured")
        
        # Recommendations
        if all_improved:
            insights["recommendations"].append("✅ Continue current data collection and model maintenance strategy")
        else:
            insights["recommendations"].append("🔍 Review recent data for anomalies or distribution shifts")
        
        if risk_ratio < 0.15:
            insights["recommendations"].append("⚠️ Low high-risk ratio - ensure all at-risk faculty are captured in data")
        
        insights["recommendations"].append("📈 Retrain models with expanded dataset to improve robust generalization")
        
        return insights
    
    def get_postmortem_summary(self, df: pd.DataFrame) -> Tuple[Dict, Dict, Dict]:
        """Get complete post-mortem analysis"""
        baseline = self.initialize_baseline()
        current = self.load_current_metrics()
        comparison = self.compare_metrics(baseline, current)
        insights = self.generate_insights(comparison, df, baseline)
        
        return baseline, comparison, insights


def format_metrics_table(comparison: Dict) -> pd.DataFrame:
    """Format comparison data for display as table"""
    rows = []
    
    for model_name, metrics in comparison.items():
        for metric in ["accuracy", "precision", "recall", "f1_score"]:
            data = metrics[metric]
            rows.append({
                "Model": model_name.replace("_", " ").title(),
                "Metric": metric.upper(),
                "Initial": f"{data['baseline']:.4f}",
                "Current": f"{data['current']:.4f}",
                "Change": f"{data['change']:+.4f} ({data['pct_change']:+.2f}%)",
                "Status": data['direction'].upper()
            })
    
    return pd.DataFrame(rows)