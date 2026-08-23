import os
import sys
import json
import joblib
import numpy as np
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)

# =========================================================
# PROJECT ROOT
# =========================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.insert(
    0,
    PROJECT_ROOT
)

# =========================================================
# PATHS
# =========================================================

DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "datasets",
    "UNSW_NB15_testing-set.parquet"
)

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "saved_models",
    "UNSW_NB15",
    "iforest_unsw.pkl"
)

SCALER_PATH = os.path.join(
    PROJECT_ROOT,
    "saved_models",
    "UNSW_NB15",
    "scaler_unsw.pkl"
)

FEATURE_PATH = os.path.join(
    PROJECT_ROOT,
    "saved_models",
    "UNSW_NB15",
    "feature_columns.json"
)

THRESHOLD_PATH = os.path.join(
    PROJECT_ROOT,
    "saved_models",
    "UNSW_NB15",
    "threshold.json"
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "logs"
)

OUTPUT_PATH = os.path.join(
    OUTPUT_DIR,
    "unsw_final_results.csv"
)

# =========================================================
# HEADER
# =========================================================

print("\n" + "=" * 70)
print("FINAL UNSW-NB15 MODEL EVALUATION")
print("=" * 70)

# =========================================================
# LOAD FEATURE CONFIGURATION
# =========================================================

print("\nLoading feature configuration...")

with open(FEATURE_PATH, "r") as f:
    feature_columns = json.load(f)

with open(THRESHOLD_PATH, "r") as f:
    threshold_config = json.load(f)

threshold = float(
    threshold_config["threshold"]
)

print("\nSelected features:")

for i, feature in enumerate(
    feature_columns,
    start=1
):
    print(
        f"{i:2}. {feature}"
    )

print(
    f"\nThreshold : {threshold:.6f}"
)

# =========================================================
# LOAD DATASET
# =========================================================

print("\nLoading UNSW-NB15 dataset...")

df = pd.read_parquet(
    DATA_PATH
)

print(
    f"Dataset Shape : {df.shape}"
)

# =========================================================
# CHECK REQUIRED COLUMNS
# =========================================================

required_columns = (
    feature_columns +
    ["label"]
)

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    raise RuntimeError(
        "Missing required columns: "
        + str(missing_columns)
    )

# =========================================================
# CLEAN DATA
# =========================================================

df = df.replace(
    [np.inf, -np.inf],
    np.nan
)

df = df.dropna(
    subset=required_columns
)

print(
    f"Clean dataset shape : {df.shape}"
)

# =========================================================
# PREPARE FEATURES
# =========================================================

X = df[
    feature_columns
].copy()

y = df[
    "label"
].astype(int)

# Ensure numerical values
X = X.apply(
    pd.to_numeric,
    errors="coerce"
)

valid_rows = (
    X.notna().all(axis=1)
)

X = X.loc[
    valid_rows
]

y = y.loc[
    valid_rows
]

X = X.reset_index(
    drop=True
)

y = y.reset_index(
    drop=True
)

print(
    f"Evaluation samples : {len(X)}"
)

print(
    f"Feature count      : {X.shape[1]}"
)

# =========================================================
# LOAD MODEL
# =========================================================

print("\nLoading trained Isolation Forest...")

model = joblib.load(
    MODEL_PATH
)

print("✓ Model loaded")

# =========================================================
# LOAD SCALER
# =========================================================

print("\nLoading training scaler...")

scaler = joblib.load(
    SCALER_PATH
)

print("✓ Scaler loaded")

# =========================================================
# VERIFY FEATURE COUNT
# =========================================================

if X.shape[1] != len(feature_columns):

    raise RuntimeError(
        "Feature count mismatch."
    )

# =========================================================
# SCALE FEATURES
# =========================================================

print("\nScaling features...")

# ---------------------------------------------------------
# The scaler was trained on ALL 31 numeric features.
# We must reproduce that preprocessing before selecting
# the final Top-10 features.
# ---------------------------------------------------------

scaler_features = list(
    scaler.feature_names_in_
)

print(
    f"Scaler expects : {len(scaler_features)} features"
)

# Verify all scaler features exist in the dataset
missing_scaler_features = [
    feature
    for feature in scaler_features
    if feature not in df.columns
]

if missing_scaler_features:

    raise RuntimeError(
        "Dataset is missing scaler features: "
        + str(missing_scaler_features)
    )

# ---------------------------------------------------------
# Prepare the complete 31-feature input for scaler
# ---------------------------------------------------------

X_scaler = df[
    scaler_features
].copy()

X_scaler = X_scaler.apply(
    pd.to_numeric,
    errors="coerce"
)

# Remove rows that became invalid
valid_rows = X_scaler.notna().all(axis=1)

X_scaler = X_scaler.loc[
    valid_rows
].reset_index(drop=True)

y = df.loc[
    valid_rows,
    "label"
].astype(int).reset_index(drop=True)

# ---------------------------------------------------------
# Scale ALL features expected by scaler
# ---------------------------------------------------------

X_scaled_all = scaler.transform(
    X_scaler
)

print(
    f"Scaled full shape : {X_scaled_all.shape}"
)

# ---------------------------------------------------------
# Find the positions of our final Top-10 features
# ---------------------------------------------------------

feature_indices = [
    scaler_features.index(feature)
    for feature in feature_columns
]

# ---------------------------------------------------------
# Select final Top-10 AFTER scaling
# ---------------------------------------------------------

X_scaled = X_scaled_all[
    :,
    feature_indices
]

print(
    f"Final model input shape : {X_scaled.shape}"
)

print(
    f"Final model features    : {len(feature_columns)}"
)

# =========================================================
# MODEL SCORING
# =========================================================

print("\nRunning predictions...")

scores = model.decision_function(
    X_scaled
)

# Isolation Forest:
# lower score = more anomalous

predictions = (
    scores < threshold
).astype(int)

# =========================================================
# METRICS
# =========================================================

accuracy = accuracy_score(
    y,
    predictions
)

precision = precision_score(
    y,
    predictions,
    zero_division=0
)

recall = recall_score(
    y,
    predictions,
    zero_division=0
)

f1 = f1_score(
    y,
    predictions,
    zero_division=0
)

roc_auc = roc_auc_score(
    y,
    -scores
)

# =========================================================
# DISPLAY RESULTS
# =========================================================

print("\n" + "=" * 70)
print("UNSW-NB15 MODEL PERFORMANCE")
print("=" * 70)

print(
    f"Samples      : {len(X)}"
)

print(
    f"Features     : {len(feature_columns)}"
)

print(
    f"Threshold    : {threshold:.6f}"
)

print(
    f"Accuracy     : {accuracy:.4f}"
)

print(
    f"Precision    : {precision:.4f}"
)

print(
    f"Recall       : {recall:.4f}"
)

print(
    f"F1 Score     : {f1:.4f}"
)

print(
    f"ROC-AUC      : {roc_auc:.4f}"
)

print("\nClassification Report:\n")

print(
    classification_report(
        y,
        predictions,
        digits=4,
        zero_division=0
    )
)

# =========================================================
# SAVE RESULTS
# =========================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

results_df = pd.DataFrame({

    "score": scores,

    "threshold": threshold,

    "prediction": predictions,

    "true_label": y

})

results_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print(
    f"\nResults saved to:"
)

print(
    OUTPUT_PATH
)

print("\n" + "=" * 70)
print("EVALUATION COMPLETE")
print("=" * 70)