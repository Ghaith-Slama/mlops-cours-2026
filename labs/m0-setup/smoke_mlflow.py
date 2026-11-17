#!/usr/bin/env python3
"""Smoke test MLflow : création d'un run avec un artefact."""

import mlflow
import tempfile
import os

# Configuration depuis .env
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))

# Créer une expérience de test
experiment_name = "hello-mlops"
try:
    experiment_id = mlflow.create_experiment(experiment_name)
except Exception:
    experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id

mlflow.set_experiment(experiment_name)

# Run avec un artefact
with mlflow.start_run(run_name="smoke-test"):
    mlflow.log_param("test", "smoke")
    mlflow.log_metric("dummy", 42)
    
    # Créer et logger un artefact SANS subfolder
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Hello from MLflow smoke test!\n")
        artifact_path = f.name
    
    # Log as "hello.txt" directly (no subfolder)
    mlflow.log_artifact(artifact_path, artifact_path="hello.txt")
    os.unlink(artifact_path)
    
    print("✅ MLflow run créé avec succès!")
    print(f"   Experiment: {experiment_name}")
    print(f"   Run ID: {mlflow.active_run().info.run_id}")
