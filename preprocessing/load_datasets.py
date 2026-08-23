import pandas as pd
import os
from scipy.io import arff

# =========================
# BASE PATH
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# =========================
# LOAD CICIDS2017
# =========================
def load_cicids():
    path = os.path.join(
        BASE_DIR,
        "datasets",
        "CICIDS2017",
        "Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"
    )

    df = pd.read_csv(path)

    print("\nCICIDS2017 Loaded")
    print(df.shape)

    return df

# =========================
# LOAD UNSW-NB15
# =========================
def load_unsw():
    train_path = os.path.join(
        BASE_DIR,
        "datasets",
        "UNSW_NB15",
        "UNSW_NB15_training-set.csv"
    )
    test_path = os.path.join(
        BASE_DIR,
        "datasets",
        "UNSW_NB15",
        "UNSW_NB15_testing-set.csv"
    )

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    df = pd.concat([train_df, test_df], ignore_index=True)

    print("\nUNSW-NB15 Loaded")
    print(df.shape)

    return df

# =========================
# LOAD NSL-KDD FROM ARFF
# =========================
def load_nslkdd():
    path = os.path.join(
        BASE_DIR,
        "datasets",
        "NSL_KDD",
        "KDDTest+.arff"
    )

    data, meta = arff.loadarff(path)
    df = pd.DataFrame(data)

    # Decode byte strings into normal strings
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].apply(
                lambda x: x.decode("utf-8") if isinstance(x, bytes) else x
            )

    print("\nNSL-KDD ARFF Loaded")
    print(df.shape)

    return df

# =========================
# SAVE NSL-KDD TO CSV
# =========================
def save_nslkdd(df):
    output_path = os.path.join(
        BASE_DIR,
        "datasets",
        "NSL_KDD",
        "KDDTest+.csv"
    )

    df.to_csv(output_path, index=False)

    print("\nNSL-KDD Converted to CSV")
    print(output_path)

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    cicids = load_cicids()
    unsw = load_unsw()
    nslkdd = load_nslkdd()
    save_nslkdd(nslkdd)