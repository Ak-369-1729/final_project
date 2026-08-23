import joblib

# Load models
cicids_model = joblib.load("models/cicids_model.pkl")
unsw_model = joblib.load("models/unsw_model.pkl")
nsl_model = joblib.load("models/nsl_model.pkl")

# Load scalers
cicids_scaler = joblib.load("scalers/cicids_scaler.pkl")
unsw_scaler = joblib.load("scalers/unsw_scaler.pkl")
nsl_scaler = joblib.load("scalers/nsl_scaler.pkl")

print("✅ All models and scalers loaded successfully")