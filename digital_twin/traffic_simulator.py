import random
import time
import pandas as pd

# =========================================================
# NODE LIST
# =========================================================
DEVICES = [
    "Node_A",
    "Node_B",
    "Node_C",
    "Node_D",
    "Node_E"
]

# =========================================================
# PROTOCOLS
# =========================================================
PROTOCOLS = [
    "TCP",
    "UDP",
    "ICMP"
]

# =========================================================
# SERVICES
# =========================================================
SERVICES = [
    "http",
    "ftp",
    "dns",
    "ssh"
]

# =========================================================
# STATES
# =========================================================
STATES = [
    "CON",
    "FIN",
    "REQ",
    "INT"
]

# =========================================================
# GENERATE TRAFFIC SAMPLE
# =========================================================
def generate_traffic():

    source = random.choice(DEVICES)

    destination = random.choice(
        [d for d in DEVICES if d != source]
    )

    # -----------------------------------------------------
    # NORMAL VS ATTACK TRAFFIC
    # -----------------------------------------------------
    is_attack = random.random() < 0.25

    if is_attack:

        packet_size = random.randint(1200, 5000)

        duration = round(
            random.uniform(5.0, 20.0),
            2
        )

        src_bytes = random.randint(5000, 50000)

        dst_bytes = random.randint(5000, 50000)

    else:

        packet_size = random.randint(50, 1500)

        duration = round(
            random.uniform(0.1, 3.0),
            2
        )

        src_bytes = random.randint(100, 5000)

        dst_bytes = random.randint(100, 5000)

    # -----------------------------------------------------
    # TRAFFIC RECORD
    # -----------------------------------------------------
    traffic = {

        "source": source,

        "destination": destination,

        "proto": random.choice(PROTOCOLS),

        "service": random.choice(SERVICES),

        "state": random.choice(STATES),

        "packet_size": packet_size,

        "duration": duration,

        "src_bytes": src_bytes,

        "dst_bytes": dst_bytes
    }

    return traffic

# =========================================================
# STREAM TRAFFIC
# =========================================================
def stream_traffic(delay=1):

    while True:

        traffic = generate_traffic()

        df = pd.DataFrame([traffic])

        print("\nGenerated Traffic:\n")

        print(df)

        time.sleep(delay)

# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":

    stream_traffic()