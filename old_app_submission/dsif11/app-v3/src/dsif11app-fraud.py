

path_python_material = ".." # REPLACE WITH YOUR PATH
model_id = "lr1"


# If unsure, print current directory path by executing the following in a new cell:
# !pwd

import numpy as np
import pickle
from fastapi import FastAPI
from pydantic import BaseModel
import shap
import sys
import pandas as pd
from typing import List
import datetime


sys.path.insert(0, '../')

app = FastAPI()

# Load the pipeline
with open(f"{path_python_material}/models/{model_id}-pipeline.pkl", "rb") as f:
    loaded_pipeline = pickle.load(f)

class Transaction(BaseModel):
    transaction_amount: float
    customer_age: int
    customer_balance: float

# Define the batch model, now referencing the already-defined Transaction class
class TransactionsBatch(BaseModel):
    transactions: List[Transaction]


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

@app.post('/predict_automation')
def predict_automation(files_to_process:List[str]):

    from conf.conf import landing_path_input_data, landing_path_output_data

    print(f"Files to process (beginning): {files_to_process}")
    if '.DS_Store' in files_to_process:
        files_to_process.remove('.DS_Store')
        print(f"Files to process: {files_to_process}")

    input_data = pd.concat([pd.read_csv(landing_path_input_data + "/" + f) for f in files_to_process], ignore_index=True, sort=False)

    # # generate predictions
    input_data['pred_fraud'] = loaded_pipeline.predict(input_data)
    input_data['pred_proba_fraud'] = loaded_pipeline.predict_proba(input_data.drop(columns=['pred_fraud']))[:, 1]
    input_data['pred_proba_fraud'] = input_data['pred_proba_fraud'].apply(lambda x: round(x, 5))

    now = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    input_data.to_csv(landing_path_output_data + "/api_tagged_" + now + ".csv", index=False)
    return {
        "Predictions saved in " + landing_path_output_data + "/api_tagged_" + now + ".csv"
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

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)


@app.post("/predict_batch/")
def predict_batch(transactions_batch: TransactionsBatch):
    # Prepare predictions list
    predictions = []

    # Loop through each transaction in the batch
    for transaction in transactions_batch.transactions:
        data_point = np.array([[
            transaction.transaction_amount,
            transaction.customer_age,
            transaction.customer_balance
        ]])

        # Make predictions
        prediction = loaded_pipeline.predict(data_point)
        confidence = loaded_pipeline.predict_proba(data_point)[0].tolist()

        # Store the prediction and confidence
        predictions.append({
            "fraud_prediction": int(prediction[0]),
            "confidence": confidence
        })

    # Return all predictions
    return predictions