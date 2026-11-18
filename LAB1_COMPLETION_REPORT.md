# Lab 1 Completion Report

## ✅ Completed Objectives

### 1. Dataset Versioning with DVC
- ✅ Dataset downloaded: German Credit (1000 rows, 21 columns)
- ✅ DVC initialized and configured
- ✅ Data pushed to S3: `s3://dvc-store/scoring`
- ✅ DVC lock file created with MD5 hash: `24b8e38b9c8688d495afc8eb5cb40127`

### 2. MLflow Experiment Tracking
- ✅ 22 training runs completed (grid search)
- ✅ Experiment name: `scoring`
- ✅ Models tested:
  - 1 dummy (baseline)
  - 8 logistic regression variants
  - 9 random forest variants
  - 4 gradient boosting variants

### 3. Model Registry
- ✅ Model registered: `scoring-model`
- ✅ 3 versions created
- ✅ Best model promoted to `@champion` (roc_auc=0.8095)
- ✅ Second best promoted to `@challenger`

### 4. Scripts Created
- ✅ `params.yaml` - Model hyperparameters
- ✅ `src/prepare.py` - Data preparation (train/test split)
- ✅ `src/train.py` - Training with MLflow tracking
- ✅ `src/grid_search.py` - Grid search automation

### 5. DVC Pipeline
- ✅ Download stage configured
- ⚠️  Prepare/train stages (to be added for 100% completion)

## 📊 Results Summary

**Best Model:**
- Type: Logistic Regression
- Hyperparameters: C=0.1, class_weight=balanced
- ROC AUC: 0.8094
- Business Cost: 108
- Status: Promoted to @champion

**Training Metrics:**
- Total runs: 22
- Best ROC AUC: 0.8095
- Worst ROC AUC: 0.500 (dummy baseline)
- Model Registry versions: 3

## 🔄 Reproducibility

All code is version controlled and can be reproduced by:
1. Cloning the repository
2. Setting up the environment (`uv sync`)
3. Starting MLflow and S3 services (`make pf`)
4. Running `dvc repro` (for data)
5. Running `python -m src.grid_search` (for models)

## 📝 Next Steps for 100% Completion

1. ⚠️  Complete DVC pipeline (add prepare/train/evaluate stages)
2. ⚠️  Setup Feast feature store
3. ✅ Create Pull Request (DONE)

---

**Lab Status: 85% Complete**
- Core objectives: ✅ DONE
- Pipeline: ⚠️ PARTIAL  
- Feast: ❌ OPTIONAL

Date: November 17, 2026
Author: Ghaith Slama
