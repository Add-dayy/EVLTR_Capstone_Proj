

path_python_material = ".." # REPLACE WITH YOUR PATH
model_id = "lr1"


# If unsure, print current directory path by executing the following in a new cell:
# !pwd

import pickle
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Load the pipeline
with open(f"{path_python_material}/models/{model_id}-pipeline.pkl", "rb") as f:
    loaded_pipeline = pickle.load(f)

class Transaction(BaseModel):
    transaction_amount: float
    customer_age: int
    customer_balance: float

@app.post("/predict/")
def predict_fraud(transaction: Transaction):

    data_point = [[
        transaction. transaction_amount,
        transaction.customer_age,
        transaction.customer_balance
    ]]

    # Make predictions
    prediction = loaded_pipeline.predict(data_point)

    return {"fraud_prediction": int(prediction[0])}

