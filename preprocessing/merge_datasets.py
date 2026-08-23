from load_datasets import load_cicids, load_unsw, load_nslkdd
from clean_data import clean_dataset
from feature_engineering import scale_features

import pandas as pd


# =========================
# LOAD DATASETS
# =========================

cicids = load_cicids()
unsw = load_unsw()
nslkdd = load_nslkdd()


# =========================
# CLEAN DATASETS
# =========================

cicids = clean_dataset(cicids)
unsw = clean_dataset(unsw)
nslkdd = clean_dataset(nslkdd)


# =========================
# SCALE DATASETS
# =========================

cicids = scale_features(cicids)
unsw = scale_features(unsw)
nslkdd = scale_features(nslkdd)


# =========================
# ADD DATASET SOURCE LABEL
# =========================

cicids['dataset'] = 'CICIDS2017'
unsw['dataset'] = 'UNSW_NB15'
nslkdd['dataset'] = 'NSL_KDD'


# =========================
# SAVE CLEAN DATASETS
# =========================

cicids.to_csv("datasets/CICIDS2017_cleaned.csv", index=False)

unsw.to_csv("datasets/UNSW_NB15_cleaned.csv", index=False)

nslkdd.to_csv("datasets/NSL_KDD_cleaned.csv", index=False)

print("\nAll datasets cleaned and saved successfully!")