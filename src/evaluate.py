"""Evaluate trained model on test set."""
import json
import mlflow
from pathlib import Path
from src.dataset_config import load_config
from sklearn.metrics import roc_auc_score, average_precision_score, precision_score, recall_score

def main():
    cfg = load_config()
    
    # Load test data
    X_test, y_test = cfg.read_xy("data/processed/test.csv")
    
    # Load model from MLflow format directory
    model = mlflow.sklearn.load_model("models/model")
    
    # Predict
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_pred_proba >= 0.5).astype(int)
    
    # Compute metrics
    metrics = {
        "test_roc_auc": float(roc_auc_score(y_test, y_pred_proba)),
        "test_avg_precision": float(average_precision_score(y_test, y_pred_proba)),
        "test_precision": float(precision_score(y_test, y_pred)),
        "test_recall": float(recall_score(y_test, y_pred))
    }
    
    # Save metrics
    Path("reports").mkdir(exist_ok=True)
    with open("reports/test_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    
    print(f"Test ROC AUC: {metrics['test_roc_auc']:.4f}")
    print(f"Test Avg Precision: {metrics['test_avg_precision']:.4f}")

if __name__ == "__main__":
    main()
