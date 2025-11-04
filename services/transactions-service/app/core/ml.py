import os
import joblib
import numpy as np
from typing import List


# -------------------------------------------------
# Load trained model
# -------------------------------------------------
def get_model(model_path: str = "ml/model.joblib"):
    """
    Loads a trained ML model for expense category prediction.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}. Please train or add it.")
    return joblib.load(model_path)


# -------------------------------------------------
# Predict category for a transaction description
# -------------------------------------------------
def predict_category(description: str, model=None) -> str:
    """
    Uses the ML model to predict the expense category based on transaction description.
    """
    if model is None:
        model = get_model()

    try:
        # Dummy example: if your model expects vectorized text input
        # Here we use a simple fallback for demonstration
        X_input = np.array([description])
        prediction = model.predict(X_input)
        return prediction[0]
    except Exception as e:
        print(f"⚠️ ML prediction error: {e}")
        return "Uncategorized"


# -------------------------------------------------
# Batch predict for multiple transactions
# -------------------------------------------------
def predict_categories_bulk(descriptions: List[str], model=None) -> List[str]:
    """
    Predicts categories for multiple transaction descriptions.
    """
    if model is None:
        model = get_model()

    try:
        X_input = np.array(descriptions)
        predictions = model.predict(X_input)
        return predictions.tolist()
    except Exception as e:
        print(f"⚠️ ML bulk prediction error: {e}")
        return ["Uncategorized"] * len(descriptions)
