

path_python_material = ".." # REPLACE WITH YOUR PATH
model_id = "lr1"


# If unsure, print current directory path by executing the following in a new cell:
# !pwd

import numpy as np
import pickle
from fastapi import FastAPI
from pydantic import BaseModel
import shap


app = FastAPI()

# Load the pipeline
with open(f"{path_python_material}/models/{model_id}-pipeline.pkl", "rb") as f:
    loaded_pipeline = pickle.load(f)

class Transaction(BaseModel):
    transaction_amount: float
    customer_age: int
    customer_balance: float

# Route to get feature importance
@app.get("/feature-importance")
def get_feature_importance():
    importance = loaded_pipeline[1].coef_[0].tolist()
    features = ['transaction_a  mount', 'customer_age', 'customer_balance']
    feature_importance = dict(zip(features, importance))
    return {"feature_importance": feature_importance}

# Route to predict new observations
@app.post("/predict/")
def predict_fraud(transaction: Transaction):

    data_point = np.array([[
        transaction.transaction_amount,
        transaction.customer_age,
        transaction.customer_balance
    ]])

    # Make predictions
    prediction = loaded_pipeline.predict(data_point)

    # Get probabilities for each class
    probabilities = loaded_pipeline.predict_proba(data_point)
    confidence = probabilities[0].tolist()

    # Shap values
    path = f"{path_python_material}/data/2-intermediate/dsif11-X_train_scaled.npy"
    print(path)
    X_train_scaled = np.load(path)
    explainer = shap.LinearExplainer(loaded_pipeline[1], X_train_scaled)
    shap_values = explainer.shap_values(data_point)
    print("SHAP", shap_values.tolist())

    return {
        "fraud_prediction": int(prediction[0]),
        "confidence": confidence,
        "shap_values": shap_values.tolist(),
        "features": ['transaction_amount', 'customer_age', 'customer_balance']
        }

# Endpoint for feature importance
@app.get("/feature-importance/")
def get_feature_importance():
    # Coefficients for logistic regression
    importance = loaded_pipeline[1].coef_[0]
    feature_names = ["transaction_amount", "customer_age", "customer_balance"]

    # Return feature importance as a dictionary
    feature_importance = dict(zip(feature_names, importance))
    return {"feature_importance": feature_importance}