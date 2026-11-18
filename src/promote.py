"""Promote best models to registry with @champion and @challenger aliases."""
from mlflow import MlflowClient
from src.dataset_config import load_config

def main():
    cfg = load_config()
    client = MlflowClient()
    
    # Get experiment
    experiment = client.get_experiment_by_name("scoring")
    if not experiment:
        print("No 'scoring' experiment found")
        return
    
    # Get best runs sorted by primary metric
    runs = client.search_runs(
        [experiment.experiment_id],
        filter_string="attributes.status = 'FINISHED'",
        order_by=[f"metrics.{cfg.primary_metric} DESC"],
        max_results=10
    )
    
    # Filter runs that have the primary metric
    valid_runs = [r for r in runs if cfg.primary_metric in r.data.metrics]
    
    if len(valid_runs) < 2:
        print(f"Only {len(valid_runs)} valid runs found, need at least 2")
        return
    
    model_name = "scoring-model"
    
    # Register or get existing model
    try:
        client.get_registered_model(model_name)
    except:
        client.create_registered_model(model_name)
    
    # Register top runs as versions
    registered_versions = []
    for run in valid_runs[:3]:  # Top 3 runs
        score = run.data.metrics.get(cfg.primary_metric)
        if score is None:
            continue
            
        model_uri = f"runs:/{run.info.run_id}/model"
        
        try:
            # Register model version
            mv = client.create_model_version(
                name=model_name,
                source=model_uri,
                run_id=run.info.run_id
            )
            registered_versions.append((mv, score))
            print(f"✓ Registered version {mv.version} (score: {score:.4f})")
        except Exception as e:
            # Version might already exist
            print(f"  Version for run {run.info.run_id[:8]} already registered")
            continue
    
    # Get all versions
    all_versions = client.search_model_versions(f"name='{model_name}'")
    
    if not all_versions:
        print("No versions found")
        return
    
    # Sort by score
    versions_with_scores = []
    for mv in all_versions:
        run = client.get_run(mv.run_id)
        score = run.data.metrics.get(cfg.primary_metric, 0)
        versions_with_scores.append((mv, score))
    
    versions_with_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Set champion (best score above threshold)
    for mv, score in versions_with_scores:
        if score >= cfg.promotion_threshold:
            client.set_registered_model_alias(model_name, "champion", mv.version)
            print(f"🏆 Set version {mv.version} as @champion (score: {score:.4f})")
            break
    
    # Set challenger (second best)
    if len(versions_with_scores) >= 2:
        mv, score = versions_with_scores[1]
        client.set_registered_model_alias(model_name, "challenger", mv.version)
        print(f"🥈 Set version {mv.version} as @challenger (score: {score:.4f})")

if __name__ == "__main__":
    main()
