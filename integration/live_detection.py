import os
import sys
import time
import random
import warnings
import joblib
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# =========================================================
# PROJECT ROOT PATH
# =========================================================
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

# =========================================================
# IMPORTS
# =========================================================
from anomaly_detection.dynamic_iforest import DynamicIsolationForest

from node_isolation.isolation_engine import (
    isolate_node,
    restore_node,
    save_isolated_nodes,
    get_isolated_nodes
)

from digital_twin.network_topology import (
    create_network,
    draw_network
)
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_curve,
    auc
)

import matplotlib.pyplot as plt
# =========================================================
# PATHS
# =========================================================
DATA_PATH = "datasets/UNSW_NB15_testing-set.parquet"

MODEL_PATH = "saved_models/UNSW_NB15/iforest_unsw.pkl"

SCALER_PATH = "saved_models/UNSW_NB15/scaler_unsw.pkl"

ENCODER_PATH = "saved_models/UNSW_NB15/encoders.pkl"

FEATURE_PATH = "saved_models/UNSW_NB15/feature_columns.json"

OUTPUT_PATH = "logs/live_node_status.csv"

ATTACK_LOG_PATH = "logs/live_attack_log.csv"

# =========================================================
# SLIDING WINDOW CONFIG
# =========================================================
WINDOW_SIZE = 1000

THRESHOLD_UPDATE_INTERVAL = 50

# =========================================================
# LOAD DATASET
# =========================================================
print("\nLoading UNSW-NB15 dataset...")

df = pd.read_parquet(DATA_PATH)

print(f"\nDataset Shape: {df.shape}")

# Lightweight real-time simulation
df = df.sample(500, random_state=42)


# Labels
y = df["label"]

# Features
X = df.drop(columns=["label", "attack_cat"])
from sklearn.preprocessing import LabelEncoder

for col in ["proto", "service", "state"]:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))

print("Feature count:", len(X.columns))
print(X.columns.tolist())


# Fix feature mismatch


X = X.values
y = y.values


# =========================================================
# CREATE DIGITAL TWIN NETWORK
# =========================================================
G = create_network()

# =========================================================
# NODE DEFINITIONS
# =========================================================
nodes = [
    "Node_A",
    "Node_B",
    "Node_C",
    "Node_D",
    "Node_E"
]

# =========================================================
# NODE STATUS TRACKER
# =========================================================
node_status = {

    node: {

        "state": "ACTIVE",

        "risk": "LOW",

        "anomaly_score": 0.0,

        "attacks_detected": 0

    }

    for node in nodes
}

# =========================================================
# LOAD MODEL
# =========================================================

print("\nLoading trained model...")

unsw_model = joblib.load(
    "models/unsw_model.pkl"
)

unsw_scaler = joblib.load(
    "scalers/unsw_scaler.pkl"
)

print("Model loaded successfully!")

# =========================================
# RUN DETECTION
# =========================================

# Calculate threshold ONCE

all_scores = unsw_model.decision_function(
    unsw_scaler.transform(X)
)

dynamic_threshold = np.percentile(
    all_scores,
    10
)

print(f"\nGlobal Threshold = {dynamic_threshold:.4f}")

# Process traffic

for sample, label in zip(X, y):

    node = random.choice(nodes)

    

    sample_scaled = unsw_scaler.transform(
        [sample]
    )

    score = unsw_model.decision_function(
        sample_scaled
    )[0]
    if score < dynamic_threshold:

        risk = "HIGH"

        pass

        isolate_node(node)

    else:

        risk = "LOW"

    node_status[node] = {
        "risk": risk,
        "anomaly_score": float(score)
    }

    # Update node status
    node_status[node] = {
        "risk": risk,
        "anomaly_score": float(score)
    }

# =========================================
# MODEL EVALUATION
# =========================================

y_pred = []
scores = []

for sample in X:

    sample_scaled = unsw_scaler.transform(
        [sample]
    )

    score = unsw_model.decision_function(
        sample_scaled
    )[0]

    scores.append(score)

    if score < dynamic_threshold:
        y_pred.append(1)
    else:
        y_pred.append(0)

print("\n" + "="*50)
print("MODEL PERFORMANCE")
print("="*50)

accuracy = accuracy_score(y, y_pred)
precision = precision_score(y, y_pred)
recall = recall_score(y, y_pred)
f1 = f1_score(y, y_pred)

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")

print("\nClassification Report:\n")

print(
    classification_report(
        y,
        y_pred
    )
)

# =========================================
# CONFUSION MATRIX
# =========================================

cm = confusion_matrix(
    y,
    y_pred
)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm
)

disp.plot()

plt.title(
    "UNSW-NB15 Confusion Matrix"
)

plt.show()

# =========================================
# ROC CURVE
# =========================================

fpr, tpr, _ = roc_curve(
    y,
    [-s for s in scores]
)

roc_auc = auc(
    fpr,
    tpr
)

print(
    f"\nROC-AUC : {roc_auc:.4f}"
)

plt.figure()

plt.plot(
    fpr,
    tpr,
    label=f"AUC = {roc_auc:.4f}"
)

plt.plot(
    [0, 1],
    [0, 1],
    "--"
)

plt.xlabel(
    "False Positive Rate"
)

plt.ylabel(
    "True Positive Rate"
)

plt.title(
    "ROC Curve"
)

plt.legend()

plt.show()
# =========================================
# SAVE NODE STATUS
# =========================================

status_df = pd.DataFrame(node_status).T

status_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ---------------------------------------------------------
# SAVE ISOLATED NODES
# ---------------------------------------------------------
save_isolated_nodes(
    "logs/isolated_nodes.csv"
)

# =========================================================
# FINAL SUMMARY
# =========================================================
print("\n" + "=" * 60)

print("LIVE DIGITAL TWIN SUMMARY")

print("=" * 60)

print(f"Samples Processed : {len(X)}")

high_risk_count = sum(
    1
    for node in node_status.values()
    if node["risk"] == "HIGH"
)

print(
    f"High Risk Nodes : "
    f"{high_risk_count}"
)

print(f"Window Size       : {WINDOW_SIZE}")

print(
    f"Threshold Updates : "
    f"Every {THRESHOLD_UPDATE_INTERVAL} samples"
)

print(
    f"Final Threshold   : "
    f"{dynamic_threshold:.6f}"
)

print(
    f"Isolated Nodes    : "
    f"{get_isolated_nodes()}"
)

print("=" * 60)

# =========================================================
# DISPLAY NETWORK GRAPH
# =========================================================
draw_network(
    G,
    node_status=node_status,
    anomaly_nodes=get_isolated_nodes()
)

# =========================================================
# FINAL NODE STATUS
# =========================================================
print("\nFinal Node Status:\n")

print(status_df)