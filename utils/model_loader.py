import joblib
import json

def load_model(dataset_name):

    if dataset_name == "CICIDS2017":

        model = joblib.load(
            "saved_models/CICIDS2017/iforest_cicids.pkl"
        )

        scaler = joblib.load(
            "saved_models/CICIDS2017/scaler_cicids.pkl"
        )

        encoder = joblib.load(
            "saved_models/CICIDS2017/encoders.pkl"
        )

        with open(
            "saved_models/CICIDS2017/feature_columns.json",
            "r"
        ) as f:

            features = json.load(f)

    elif dataset_name == "UNSW_NB15":

        model = joblib.load(
            "saved_models/UNSW_NB15/iforest_unsw.pkl"
        )

        scaler = joblib.load(
            "saved_models/UNSW_NB15/scaler_unsw.pkl"
        )

        encoder = joblib.load(
            "saved_models/UNSW_NB15/encoders.pkl"
        )

        with open(
            "saved_models/UNSW_NB15/feature_columns.json",
            "r"
        ) as f:

            features = json.load(f)

    elif dataset_name == "NSL_KDD":

        model = joblib.load(
            "saved_models/NSL_KDD/iforest_nslkdd.pkl"
        )

        scaler = joblib.load(
            "saved_models/NSL_KDD/scaler_nslkdd.pkl"
        )

        encoder = joblib.load(
            "saved_models/NSL_KDD/encoders.pkl"
        )

        with open(
            "saved_models/NSL_KDD/feature_columns.json",
            "r"
        ) as f:

            features = json.load(f)

    else:

        raise ValueError("Invalid dataset")

    return model, scaler, encoder, features