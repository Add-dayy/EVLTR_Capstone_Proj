

import streamlit as st
import requests

st.title("Fraud Detection App")

transaction_amount = st.number_input("Transaction Amount")
customer_age = st.number_input("Customer Age")
customer_balance = st.number_input("Customer Balance")

if st.button("Predict"):
    response = requests.post("http://localhost:8502/predict/",
                             json={
                                 "transaction_amount": transaction_amount,
                                 "customer_age": customer_age,
                                 "customer_balance": customer_balance
                             })
    result = response.json()
    
    if result['fraud_prediction'] == 0:
        st.write("Prediction: Not fraudulent")
    else:
        st.write("Prediction: Fraudulent")


