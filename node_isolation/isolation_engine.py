import os
from datetime import datetime

import pandas as pd

# =========================================================
# GLOBAL STORAGE
# =========================================================
isolated_nodes = set()

isolation_history = []

# =========================================================
# ISOLATE NODE
# =========================================================
def isolate_node(
    node,
    risk="HIGH",
    reason="Anomaly Detected",
    node_status=None
):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ---------------------------------------------
    # PREVENT DUPLICATE ISOLATION
    # ---------------------------------------------
    if node not in isolated_nodes:

        isolated_nodes.add(node)

        print("\n" + "=" * 60)
        print(f"ALERT: NODE ISOLATED -> {node}")
        print(f"Risk Level : {risk}")
        print(f"Reason     : {reason}")
        print(f"Time       : {timestamp}")
        print("=" * 60)

        # -----------------------------------------
        # SAVE HISTORY
        # -----------------------------------------
        isolation_history.append({
            "timestamp": timestamp,
            "node": node,
            "action": "ISOLATED",
            "risk": risk,
            "reason": reason
        })

    # ---------------------------------------------
    # UPDATE NODE STATUS
    # ---------------------------------------------
    if node_status is not None:

        if node in node_status:

            node_status[node]["state"] = "ISOLATED"

            node_status[node]["risk"] = risk

            node_status[node]["last_update"] = timestamp

# =========================================================
# RESTORE NODE
# =========================================================
def restore_node(
    node,
    node_status=None
):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if node in isolated_nodes:

        isolated_nodes.remove(node)

        print("\n" + "=" * 60)
        print(f"INFO: NODE RESTORED -> {node}")
        print(f"Time: {timestamp}")
        print("=" * 60)

        isolation_history.append({
            "timestamp": timestamp,
            "node": node,
            "action": "RESTORED",
            "risk": "LOW",
            "reason": "Recovered"
        })

    # ---------------------------------------------
    # UPDATE STATUS
    # ---------------------------------------------
    if node_status is not None:

        if node in node_status:

            node_status[node]["state"] = "ACTIVE"

            node_status[node]["risk"] = "LOW"

            node_status[node]["last_update"] = timestamp

# =========================================================
# CHECK NODE STATUS
# =========================================================
def is_node_isolated(node):

    return node in isolated_nodes

# =========================================================
# GET ISOLATED NODES
# =========================================================
def get_isolated_nodes():

    return sorted(list(isolated_nodes))

# =========================================================
# DISPLAY ISOLATED NODES
# =========================================================
def show_isolated_nodes():

    print("\n" + "=" * 60)
    print("CURRENTLY ISOLATED NODES")
    print("=" * 60)

    if not isolated_nodes:

        print("No isolated nodes.")

        return

    for node in sorted(isolated_nodes):

        print(f"- {node}")

# =========================================================
# SAVE CURRENT ISOLATED NODES
# =========================================================
def save_isolated_nodes(
    path="logs/isolated_nodes.csv"
):

    os.makedirs(os.path.dirname(path), exist_ok=True)

    df = pd.DataFrame({
        "node": sorted(list(isolated_nodes))
    })

    df.to_csv(path, index=False)

    print(f"\nIsolated nodes saved to: {path}")

# =========================================================
# SAVE ISOLATION HISTORY
# =========================================================
def save_isolation_history(
    path="logs/isolation_history.csv"
):

    os.makedirs(os.path.dirname(path), exist_ok=True)

    history_df = pd.DataFrame(isolation_history)

    history_df.to_csv(path, index=False)

    print(f"\nIsolation history saved to: {path}")

# =========================================================
# CLEAR ALL ISOLATIONS
# =========================================================
def clear_all_isolations():

    isolated_nodes.clear()

    print("\nAll node isolations cleared.")