import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder


# =========================
# REMOVE MISSING VALUES
# =========================

def remove_missing(df):

    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    df.dropna(inplace=True)

    return df


# =========================
# REMOVE DUPLICATES
# =========================

def remove_duplicates(df):

    df.drop_duplicates(inplace=True)

    return df


# =========================
# ENCODE CATEGORICAL FEATURES
# =========================

def encode_features(df):

    encoder = LabelEncoder()

    for column in df.columns:

        if df[column].dtype == 'object':

            try:
                df[column] = encoder.fit_transform(df[column].astype(str))
            except:
                pass

    return df


# =========================
# MAIN CLEAN FUNCTION
# =========================

def clean_dataset(df):

    df = remove_missing(df)

    df = remove_duplicates(df)

    df = encode_features(df)

    return df