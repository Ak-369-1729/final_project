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
# PROJECT ROOT
# =========================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# =========================================================
# IMPORTS
# =========================================================

from anomaly_detection.dynamic_iforest import DynamicIsolationForest

from node_isolation.isolation_engine import (
    isolate_node,
    save_isolated_nodes,
    get_isolated_nodes
)

from digital_twin.network_topology import (
    create_network,
    draw_network
)

from sklearn.preprocessing import LabelEncoder

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

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


# =========================================================
# PATHS
# =========================================================

DATA_PATH = os.path.join(
    BASE_DIR,
    "datasets",
    "UNSW_NB15_testing-set.parquet"
)

LOG_DIR = os.path.join(
    BASE_DIR,
    "logs"
)

OUTPUT_PATH = os.path.join(
    LOG_DIR,
    "live_node_status.csv"
)

ATTACK_LOG_PATH = os.path.join(
    LOG_DIR,
    "live_attack_log.csv"
)

ISOLATED_PATH = os.path.join(
    LOG_DIR,
    "isolated_nodes.csv"
)

# =========================================================
# MODEL PATHS
# =========================================================

# Preferred paths from the original project.
MODEL_CANDIDATES = [
    os.path.join(
        BASE_DIR,
        "models",
        "unsw_model.pkl"
    ),
    os.path.join(
        BASE_DIR,
        "saved_models",
        "UNSW_NB15",
        "iforest_unsw.pkl"
    )
]

SCALER_CANDIDATES = [
    os.path.join(
        BASE_DIR,
        "scalers",
        "unsw_scaler.pkl"
    ),
    os.path.join(
        BASE_DIR,
        "saved_models",
        "UNSW_NB15",
        "scaler_unsw.pkl"
    )
]


def find_existing_path(candidates, name):
    """
    Return the first existing path from candidates.
    """

    for path in candidates:

        if os.path.exists(path):
            return path

    print("\nERROR: Could not find", name)

    print("\nChecked:")

    for path in candidates:
        print(" -", path)

    return None


# =========================================================
# CREATE REQUIRED DIRECTORIES
# =========================================================

os.makedirs(
    LOG_DIR,
    exist_ok=True
)


# =========================================================
# CONFIGURATION
# =========================================================

WINDOW_SIZE = 1000

THRESHOLD_UPDATE_INTERVAL = 50

SAMPLE_SIZE = 500


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
# INITIAL NODE STATUS
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
# LOAD DATASET
# =========================================================

print("\n" + "=" * 70)
print("NEXUS CYBER RESILIENCE")
print("LIVE THREAT DETECTION")
print("=" * 70)

print("\nLoading dataset...")

if not os.path.exists(DATA_PATH):

    print("\nERROR: Dataset not found:")
    print(DATA_PATH)

    sys.exit(1)


df = pd.read_parquet(
    DATA_PATH
)

print(
    f"Dataset Shape: {df.shape}"
)


# =========================================================
# SAMPLE DATA FOR SIMULATION
# =========================================================

sample_size = min(
    SAMPLE_SIZE,
    len(df)
)

df = df.sample(
    sample_size,
    random_state=42
).reset_index(
    drop=True
)


# =========================================================
# LABELS
# =========================================================

if "label" not in df.columns:

    print(
        "\nERROR: 'label' column not found."
    )

    sys.exit(1)


y = df["label"].copy()


# =========================================================
# FEATURES
# =========================================================

drop_columns = [
    "label",
    "attack_cat"
]

existing_drop_columns = [
    column
    for column in drop_columns
    if column in df.columns
]

X = df.drop(
    columns=existing_drop_columns
).copy()


# =========================================================
# ENCODE CATEGORICAL FEATURES
# =========================================================

for column in [
    "proto",
    "service",
    "state"
]:

    if column in X.columns:

        encoder = LabelEncoder()

        X[column] = encoder.fit_transform(
            X[column].astype(str)
        )


# =========================================================
# CONVERT TO NUMPY
# =========================================================

X = X.values

y = y.values


print(
    f"Samples processed: {len(X)}"
)

print(
    f"Feature count: {X.shape[1]}"
)


# =========================================================
# CREATE NETWORK
# =========================================================

try:

    G = create_network()

except Exception as e:

    print(
        "\nWarning: Network creation failed:"
    )

    print(e)

    G = None


# =========================================================
# FIND MODEL
# =========================================================

MODEL_PATH = find_existing_path(
    MODEL_CANDIDATES,
    "UNSW model"
)

SCALER_PATH = find_existing_path(
    SCALER_CANDIDATES,
    "UNSW scaler"
)


if MODEL_PATH is None:

    sys.exit(1)


if SCALER_PATH is None:

    sys.exit(1)


print(
    "\nLoading model:"
)

print(
    MODEL_PATH
)

print(
    "\nLoading scaler:"
)

print(
    SCALER_PATH
)


# =========================================================
# LOAD MODEL
# =========================================================

try:

    unsw_model = joblib.load(
        MODEL_PATH
    )

    unsw_scaler = joblib.load(
        SCALER_PATH
    )

except Exception as e:

    print(
        "\nERROR while loading model/scaler:"
    )

    print(e)

    sys.exit(1)


print(
    "\nModel loaded successfully."
)


# =========================================================
# SCALE DATA
# =========================================================

try:

    X_scaled = unsw_scaler.transform(
        X
    )

except Exception as e:

    print(
        "\nERROR: Feature mismatch between dataset and scaler."
    )

    print(e)

    sys.exit(1)


# =========================================================
# CALCULATE GLOBAL THRESHOLD
# =========================================================

try:

    all_scores = unsw_model.decision_function(
        X_scaled
    )

except Exception as e:

    print(
        "\nERROR calculating anomaly scores:"
    )

    print(e)

    sys.exit(1)


dynamic_threshold = np.percentile(
    all_scores,
    10
)


print(
    f"\nGlobal Threshold: "
    f"{dynamic_threshold:.6f}"
)


# =========================================================
# DETECTION
# =========================================================

y_pred = []

scores = []


for index, (sample, label) in enumerate(
    zip(X, y)
):

    node = random.choice(
        nodes
    )

    sample_scaled = unsw_scaler.transform(
        [sample]
    )

    score = float(
        unsw_model.decision_function(
            sample_scaled
        )[0]
    )

    scores.append(
        score
    )

    if score < dynamic_threshold:

        risk = "HIGH"

        node_status[node][
            "attacks_detected"
        ] += 1

        try:

            isolate_node(
                node
            )

        except Exception as e:

            print(
                f"Warning: Could not isolate {node}: {e}"
            )

    else:

        risk = "LOW"


    # Store latest status

    node_status[node] = {

        "state":
            "ISOLATED"
            if risk == "HIGH"
            else "ACTIVE",

        "risk":
            risk,

        "anomaly_score":
            score,

        "attacks_detected":
            node_status[node][
                "attacks_detected"
            ]

    }


    # Classification label

    if score < dynamic_threshold:

        y_pred.append(
            1
        )

    else:

        y_pred.append(
            0
        )


# =========================================================
# SAVE NODE STATUS
# =========================================================

status_df = pd.DataFrame(
    node_status
).T


status_df.to_csv(
    OUTPUT_PATH,
    index=False
)


print(
    "\nNode status saved to:"
)

print(
    OUTPUT_PATH
)


# =========================================================
# SAVE ISOLATED NODES
# =========================================================

try:

    save_isolated_nodes(
        ISOLATED_PATH
    )

except Exception as e:

    print(
        "\nWarning: Could not save isolated nodes:"
    )

    print(e)


# =========================================================
# SAVE ATTACK LOG
# =========================================================

attack_rows = []

for node in nodes:

    node_info = node_status[node]

    if node_info["risk"] == "HIGH":

        attack_rows.append({

            "node":
                node,

            "risk":
                node_info["risk"],

            "anomaly_score":
                node_info["anomaly_score"],

            "timestamp":
                pd.Timestamp.now()

        })


attack_log_df = pd.DataFrame(
    attack_rows
)


if attack_log_df.empty:

    attack_log_df = pd.DataFrame(
        columns=[
            "node",
            "risk",
            "anomaly_score",
            "timestamp"
        ]
    )


attack_log_df.to_csv(
    ATTACK_LOG_PATH,
    index=False
)


# =========================================================
# MODEL EVALUATION
# =========================================================

print(
    "\n" + "=" * 60
)

print(
    "MODEL PERFORMANCE"
)

print(
    "=" * 60
)


try:

    accuracy = accuracy_score(
        y,
        y_pred
    )

    precision = precision_score(
        y,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y,
        y_pred,
        zero_division=0
    )

    print(
        f"Accuracy  : {accuracy:.4f}"
    )

    print(
        f"Precision : {precision:.4f}"
    )

    print(
        f"Recall    : {recall:.4f}"
    )

    print(
        f"F1 Score  : {f1:.4f}"
    )

    print(
        "\nClassification Report:\n"
    )

    print(
        classification_report(
            y,
            y_pred,
            zero_division=0
        )
    )

except Exception as e:

    print(
        "\nEvaluation warning:"
    )

    print(e)


# =========================================================
# CONFUSION MATRIX
# =========================================================

try:

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

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            LOG_DIR,
            "confusion_matrix.png"
        )
    )

    plt.close()

except Exception as e:

    print(
        "\nConfusion matrix warning:"
    )

    print(e)


# =========================================================
# ROC CURVE
# =========================================================

try:

    fpr, tpr, _ = roc_curve(
        y,
        [-score for score in scores]
    )

    roc_auc = auc(
        fpr,
        tpr
    )

    print(
        f"\nROC-AUC: {roc_auc:.4f}"
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

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            LOG_DIR,
            "roc_curve.png"
        )
    )

    plt.close()

except Exception as e:

    print(
        "\nROC curve warning:"
    )

    print(e)


# =========================================================
# FINAL SUMMARY
# =========================================================

print(
    "\n" + "=" * 60
)

print(
    "LIVE DIGITAL TWIN SUMMARY"
)

print(
    "=" * 60
)

high_risk_count = sum(
    1
    for node in node_status.values()
    if node["risk"] == "HIGH"
)

print(
    f"Samples Processed : {len(X)}"
)

print(
    f"High Risk Nodes   : {high_risk_count}"
)

print(
    f"Window Size       : {WINDOW_SIZE}"
)

print(
    f"Threshold Updates : Every "
    f"{THRESHOLD_UPDATE_INTERVAL} samples"
)

print(
    f"Final Threshold   : "
    f"{dynamic_threshold:.6f}"
)

try:

    print(
        f"Isolated Nodes    : "
        f"{get_isolated_nodes()}"
    )

except Exception:

    pass


print(
    "=" * 60
)


# =========================================================
# DRAW NETWORK
# =========================================================

if G is not None:

    try:

        draw_network(
            G,
            node_status=node_status,
            anomaly_nodes=get_isolated_nodes()
        )

    except Exception as e:

        print(
            "\nNetwork visualization warning:"
        )

        print(e)


# =========================================================
# FINAL STATUS
# =========================================================

print(
    "\nFinal Node Status:\n"
)

print(
    status_df
)

print(
    "\nLive detection completed successfully."
)
