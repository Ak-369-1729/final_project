import os
import sys
import time
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Make sure required directories exist
os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)

# Start live detection in the background
detector = subprocess.Popen(
    [
        sys.executable,
        os.path.join(BASE_DIR, "integration", "live_detection.py")
    ],
    cwd=BASE_DIR
)

print("Live detection process started.")

# Give detector a little time to generate initial status
for _ in range(60):
    status_file = os.path.join(
        BASE_DIR,
        "logs",
        "live_node_status.csv"
    )

    if os.path.exists(status_file):
        print("Live node status generated.")
        break

    if detector.poll() is not None:
        print("Live detection process stopped unexpectedly.")
        break

    time.sleep(1)

# Start Streamlit
dashboard = os.path.join(
    BASE_DIR,
    "dashboard",
    "dashboard_app.py"
)

port = os.environ.get("PORT", "10000")

subprocess.run(
    [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        dashboard,
        "--server.address",
        "0.0.0.0",
        "--server.port",
        port,
        "--server.headless",
        "true",
    ],
    cwd=BASE_DIR
)
