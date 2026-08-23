import os
import sys
import time

import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


# =========================================================
# PROJECT ROOT
# =========================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(
        0,
        BASE_DIR
    )


# =========================================================
# IMPORTS
# =========================================================

from digital_twin.network_topology import (
    create_network
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Cybersecurity Digital Twin",
    layout="wide"
)


# =========================================================
# PATHS
# =========================================================

LOG_DIR = os.path.join(
    BASE_DIR,
    "logs"
)

STATUS_PATH = os.path.join(
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
# TITLE
# =========================================================

st.title(
    "AI-Based Cybersecurity Digital Twin"
)

st.markdown(
    """
    **Real-Time Threat Detection and Automatic Node Isolation**
    """
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header(
    "Dashboard Controls"
)

refresh = st.sidebar.slider(
    "Refresh Rate (seconds)",
    min_value=2,
    max_value=10,
    value=3
)


# =========================================================
# WAIT FOR LIVE DETECTION
# =========================================================

if not os.path.exists(
    STATUS_PATH
):

    st.warning(
        "Live detection is starting..."
    )

    st.info(
        "Please wait a few seconds while "
        "the cybersecurity detection engine "
        "generates the initial node status."
    )

    time.sleep(2)

    st.rerun()


# =========================================================
# LOAD NODE STATUS
# =========================================================

try:

    alerts = pd.read_csv(
        STATUS_PATH
    )

except Exception as e:

    st.error(
        f"Unable to read node status: {e}"
    )

    st.stop()


# =========================================================
# NORMALIZE COLUMN NAMES
# =========================================================

alerts.columns = [
    str(column)
    .strip()
    .lower()
    .replace(
        " ",
        "_"
    )
    for column in alerts.columns
]


# =========================================================
# VALIDATE REQUIRED COLUMNS
# =========================================================

required_columns = [
    "risk",
    "anomaly_score"
]

missing_columns = [
    column
    for column in required_columns
    if column not in alerts.columns
]

if missing_columns:

    st.error(
        "Missing required columns: "
        + ", ".join(
            missing_columns
        )
    )

    st.stop()


# =========================================================
# NODE NAMES
# =========================================================

node_names = [
    "Node_A",
    "Node_B",
    "Node_C",
    "Node_D",
    "Node_E"
]


# =========================================================
# ASSIGN NODE NAMES
# =========================================================

node_count = min(
    len(alerts),
    len(node_names)
)

alerts = alerts.iloc[
    :node_count
].copy()

alerts["node"] = node_names[
    :node_count
]


# =========================================================
# LOAD ISOLATED NODES
# =========================================================

isolated_nodes = set()


if os.path.exists(
    ISOLATED_PATH
):

    try:

        isolated_df = pd.read_csv(
            ISOLATED_PATH
        )

        if "node" in isolated_df.columns:

            isolated_nodes = set(
                isolated_df[
                    "node"
                ]
                .astype(str)
                .str.strip()
            )

    except Exception:

        isolated_nodes = set()


# =========================================================
# NODE STATE
# =========================================================

alerts["state"] = alerts[
    "node"
].apply(

    lambda node:

        "ISOLATED"
        if node in isolated_nodes
        else "ACTIVE"

)


# =========================================================
# CLEAN RISK
# =========================================================

alerts["risk"] = (

    alerts[
        "risk"
    ]
    .astype(str)
    .str.upper()
    .str.strip()

)


# =========================================================
# CLEAN ANOMALY SCORE
# =========================================================

alerts[
    "anomaly_score"
] = pd.to_numeric(

    alerts[
        "anomaly_score"
    ],

    errors="coerce"

).fillna(0.0)


# =========================================================
# ATTACK COUNT
# =========================================================

if "attacks_detected" not in alerts.columns:

    alerts[
        "attacks_detected"
    ] = 0


alerts[
    "attacks_detected"
] = pd.to_numeric(

    alerts[
        "attacks_detected"
    ],

    errors="coerce"

).fillna(0).astype(int)


# =========================================================
# FINAL DATAFRAME
# =========================================================

alerts = alerts[
    [
        "node",
        "state",
        "risk",
        "anomaly_score",
        "attacks_detected"
    ]
].copy()


# =========================================================
# NETWORK METRICS
# =========================================================

total_nodes = len(
    alerts
)

isolated_count = len(
    alerts[
        alerts["state"] == "ISOLATED"
    ]
)

high_risk = len(
    alerts[
        alerts["risk"] == "HIGH"
    ]
)

medium_risk = len(
    alerts[
        alerts["risk"] == "MEDIUM"
    ]
)


# =========================================================
# METRIC CARDS
# =========================================================

st.subheader(
    "Network Metrics"
)

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Total Nodes",
    total_nodes
)

col2.metric(
    "Isolated Nodes",
    isolated_count
)

col3.metric(
    "High Risk Nodes",
    high_risk
)

col4.metric(
    "Medium Risk Nodes",
    medium_risk
)


# =========================================================
# NETWORK TOPOLOGY
# =========================================================

st.subheader(
    "Live Network Topology"
)


try:

    G = create_network()

    fig, ax = plt.subplots(
        figsize=(12, 8)
    )

    pos = nx.spring_layout(
        G,
        seed=42
    )

    color_map = []


    # =====================================================
    # NODE COLORS
    # =====================================================

    for node in G.nodes():

        if node in alerts[
            "node"
        ].values:

            row = alerts.loc[
                alerts["node"] == node
            ].iloc[0]

            state = row[
                "state"
            ]

            risk = row[
                "risk"
            ]


            if state == "ISOLATED":

                color_map.append(
                    "red"
                )

            elif risk == "HIGH":

                color_map.append(
                    "red"
                )

            elif risk == "MEDIUM":

                color_map.append(
                    "orange"
                )

            else:

                color_map.append(
                    "green"
                )

        else:

            color_map.append(
                "lightgray"
            )


    # =====================================================
    # DRAW GRAPH
    # =====================================================

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2800,
        node_color=color_map,
        font_size=10,
        font_weight="bold",
        edge_color="gray",
        ax=ax
    )


    ax.set_title(
        "Cybersecurity Digital Twin Network",
        fontsize=14,
        fontweight="bold"
    )


    st.pyplot(
        fig
    )

    plt.close(fig)


except Exception as e:

    st.warning(
        f"Network visualization unavailable: {e}"
    )


# =========================================================
# NODE STATUS TABLE
# =========================================================

st.subheader(
    "Live Node Status"
)


display_df = alerts.rename(

    columns={

        "node":
            "Node",

        "state":
            "State",

        "risk":
            "Risk",

        "anomaly_score":
            "Anomaly Score",

        "attacks_detected":
            "Attacks Detected"

    }

)


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# ATTACK DISTRIBUTION
# =========================================================

st.subheader(
    "Attack Distribution"
)


chart_data = alerts[
    [
        "node",
        "attacks_detected"
    ]
].copy()


chart_data.columns = [
    "Node",
    "Attacks"
]


st.bar_chart(
    chart_data.set_index(
        "Node"
    )
)


# =========================================================
# ANOMALY SCORE
# =========================================================

st.subheader(
    "Anomaly Scores"
)


score_data = alerts[
    [
        "node",
        "anomaly_score"
    ]
].copy()


score_data.columns = [
    "Node",
    "Score"
]


st.line_chart(
    score_data.set_index(
        "Node"
    )
)


# =========================================================
# ATTACK LOGS
# =========================================================

st.subheader(
    "Recent Attack Logs"
)


if os.path.exists(
    ATTACK_LOG_PATH
):

    try:

        attack_logs = pd.read_csv(
            ATTACK_LOG_PATH
        )

        if len(attack_logs) > 0:

            st.dataframe(
                attack_logs.tail(20),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No attacks detected in the latest run."
            )

    except Exception as e:

        st.warning(
            f"Could not read attack logs: {e}"
        )

else:

    st.info(
        "No attack logs available yet."
    )


# =========================================================
# AUTO REFRESH
# =========================================================

time.sleep(
    refresh
)

st.rerun()
