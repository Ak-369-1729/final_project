import os
import json
import joblib
import numpy as np
import pandas as pd

# =========================================================
# HYBRID ADAPTIVE THRESHOLD
# =========================================================
def compute_hybrid_threshold(
    scores,
    k=0.5,
    percentile=40
):

    q1 = np.percentile(scores, 25)

    q3 = np.percentile(scores, 75)

    qd = (q3 - q1) / 2

    qd_threshold = q1 - (k * qd)

    percentile_threshold = np.percentile(
        scores,
        percentile
    )

    threshold = max(
        qd_threshold,
        percentile_threshold
    )

    return threshold, q1, q3, qd

# =========================================================
# DYNAMIC ISOLATION FOREST
# =========================================================
class DynamicIsolationForest:

    def __init__(
        self,
        model_path,
        scaler_path=None,
        encoder_path=None,
        feature_path=None,
        threshold=None,
        use_hybrid_threshold=True,
        k=0.5,
        percentile=40
    ):

        self.model_path = model_path

        self.scaler_path = scaler_path

        self.encoder_path = encoder_path

        self.feature_path = feature_path

        self.threshold = threshold

        self.use_hybrid_threshold = use_hybrid_threshold

        self.k = k

        self.percentile = percentile

        self.model = None

        self.scaler = None

        self.encoders = None

        self.feature_columns = None

        self.results = []

        self.load_artifacts()

    # =====================================================
    # LOAD ARTIFACTS
    # =====================================================
    def load_artifacts(self):

        if not os.path.exists(self.model_path):

            raise FileNotFoundError(
                f"Model file not found: {self.model_path}"
            )

        self.model = joblib.load(
            self.model_path
        )

        if (
            self.scaler_path
            and os.path.exists(self.scaler_path)
        ):

            self.scaler = joblib.load(
                self.scaler_path
            )

        if (
            self.encoder_path
            and os.path.exists(self.encoder_path)
        ):

            self.encoders = joblib.load(
                self.encoder_path
            )

        if (
            self.feature_path
            and os.path.exists(self.feature_path)
        ):

            with open(self.feature_path, "r") as f:

                self.feature_columns = json.load(f)

        print("\n" + "=" * 60)

        print("MODEL ARTIFACTS LOADED")

        print("=" * 60)

        print(f"Model Path   : {self.model_path}")

        print(f"Scaler Path  : {self.scaler_path}")

        print(f"Encoder Path : {self.encoder_path}")

        print(f"Feature Path : {self.feature_path}")

        print("=" * 60)

    # =====================================================
    # PREPROCESS INPUT
    # =====================================================
    def preprocess_input(
        self,
        X_input
    ):

        if isinstance(X_input, np.ndarray):

            X_df = pd.DataFrame(X_input)

        elif isinstance(X_input, pd.Series):

            X_df = X_input.to_frame().T

        else:

            X_df = X_input.copy()

        categorical_cols = [
            "protocol_type",
            "proto",
            "service",
            "flag",
            "state"
        ]

        if self.encoders is not None:

            for col in categorical_cols:

                if (
                    col in X_df.columns
                    and col in self.encoders
                ):

                    X_df[col] = X_df[col].astype(str)

                    encoder = self.encoders[col]

                    X_df[col] = X_df[col].apply(

                        lambda x: (
                            encoder.transform([x])[0]
                            if x in encoder.classes_
                            else -1
                        )
                    )

        if self.feature_columns is not None:

            for col in self.feature_columns:

                if col not in X_df.columns:

                    X_df[col] = 0

            X_df = X_df[self.feature_columns]

        X_df = X_df.apply(
            pd.to_numeric,
            errors="coerce"
        )

        X_df.fillna(0, inplace=True)

        X_processed = X_df.copy()

        if self.scaler is not None:

            X_processed = self.scaler.transform(
                X_processed
            )

        return X_processed, X_df

    # =====================================================
    # COMPUTE THRESHOLD
    # =====================================================
    def fit_threshold_on_reference(
        self,
        X_reference
    ):

        X_processed, _ = self.preprocess_input(
            X_reference
        )

        scores = self.model.decision_function(
            X_processed
        )

        if self.use_hybrid_threshold:

            (
                self.threshold,
                q1,
                q3,
                qd
            ) = compute_hybrid_threshold(
                scores,
                k=self.k,
                percentile=self.percentile
            )

            print("\n" + "=" * 60)

            print("DYNAMIC THRESHOLD COMPUTED")

            print("=" * 60)

            print(f"Samples   : {len(scores)}")

            print(f"Q1        : {q1:.6f}")

            print(f"Q3        : {q3:.6f}")

            print(f"QD        : {qd:.6f}")

            print(f"Threshold : {self.threshold:.6f}")

            print("Method    : Hybrid QD + Percentile")

            print("=" * 60)

        else:

            self.threshold = np.percentile(
                scores,
                self.percentile
            )

            print(
                f"Threshold: {self.threshold:.6f}"
            )

    # =====================================================
    # PREDICT SINGLE SAMPLE
    # =====================================================
    def predict_one(
        self,
        sample,
        label=None
    ):

        if isinstance(sample, pd.DataFrame):

            sample_df = sample.copy()

        elif isinstance(sample, pd.Series):

            sample_df = sample.to_frame().T

        else:

            sample_arr = np.array(sample)

            if sample_arr.ndim == 1:

                sample_df = pd.DataFrame(
                    [sample_arr]
                )

            else:

                sample_df = pd.DataFrame(
                    sample_arr
                )

        X_processed, _ = self.preprocess_input(
            sample_df
        )

        score = self.model.decision_function(
            X_processed
        )[0]

        prediction = (
            1 if score < self.threshold else 0
        )

        margin = abs(self.threshold) * 0.2

        if score < self.threshold:

            risk = "HIGH"

        elif score < (
            self.threshold + margin
        ):

            risk = "MEDIUM"

        else:

            risk = "LOW"

        result = {

            "score": float(score),

            "threshold": float(self.threshold),

            "prediction": int(prediction),

            "risk_level": risk,

            "true_label": label
        }

        self.results.append(result)

        return prediction, result

    # =====================================================
    # RESULTS
    # =====================================================
    def get_results_df(self):

        return pd.DataFrame(
            self.results
        )