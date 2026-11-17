#!/usr/bin/env python3
"""Smoke test MLflow : création d'un run avec un artefact."""

import mlflow
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
    
    # Créer un fichier temporaire nommé hello.txt
    artifact_file = "/tmp/hello.txt"
    with open(artifact_file, 'w') as f:
        f.write("Hello from MLflow smoke test!\n")
    
    # Log artifact (devient hello.txt à la racine)
    mlflow.log_artifact(artifact_file)
    os.unlink(artifact_file)
    
    print("✅ MLflow run créé avec succès!")
    print(f"   Experiment: {experiment_name}")
    print(f"   Run ID: {mlflow.active_run().info.run_id}")
