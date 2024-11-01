# 8503
api_url = "http://localhost:8502"

import streamlit as st
import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

st.title("Fraud Detection App")

# Display site header
image_path = "../images/dsif header 2.jpeg"
try:
    img = Image.open(image_path)
    st.image(img, use_column_width=True)
except FileNotFoundError:
    st.error(f"Image not found at {image_path}. Please check the file path.")

# Individual Transaction Input Section
st.header("Single Transaction Prediction")

transaction_amount = st.number_input("Transaction Amount")
customer_age = st.number_input("Customer Age")
customer_balance = st.number_input("Customer Balance")

data = {
    "transaction_amount": transaction_amount,
    "customer_age": customer_age,
    "customer_balance": customer_balance
}

# Feature Importance
if st.button("Show Feature Importance"):
    response = requests.get(f"{api_url}/feature-importance")
    feature_importance = response.json().get('feature_importance', {})

    features = list(feature_importance.keys())
    importance = list(feature_importance.values())

    fig, ax = plt.subplots()
    ax.barh(features, importance)
    ax.set_xlabel('Importance')
    ax.set_title('Feature Importance')
    st.pyplot(fig)

# Batch Prediction Section (File Upload)
st.header("Batch Transaction Prediction (File Upload)")

uploaded_file = st.file_uploader("Upload a CSV file with transactions", type=["csv"])

if uploaded_file is not None:
    # Read the file into a DataFrame
    df = pd.read_csv(uploaded_file)

    st.write("Uploaded File Preview:")
    st.write(df.head())

    # Check if the required columns exist in the uploaded CSV
    if all(col in df.columns for col in ['transaction_amount', 'customer_age', 'customer_balance']):

        # Create the new feature: transaction amount to balance ratio
        df['transaction_to_balance_ratio'] = df['transaction_amount'] / df['customer_balance']

        transactions_data = df[['transaction_amount', 'customer_age', 'customer_balance']].to_dict(orient='records')

        # Run Predictions for Batch
        if st.button("Run Batch Predictions"):
            response = requests.post(f"{api_url}/predict_batch/", json={"transactions": transactions_data})

            if response.status_code == 200:
                predictions = response.json()

                # Add predictions to DataFrame
                df['fraud_prediction'] = [pred['fraud_prediction'] for pred in predictions]
                df['confidence'] = [pred['confidence'] for pred in predictions]

                st.write("Predictions:")
                st.write(df.head())

                # Allow the user to download the CSV file with predictions
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download predictions as CSV",
                    data=csv,
                    file_name="fraud_predictions.csv",
                    mime='text/csv',
                )
            else:
                st.error(f"Error: {response.status_code}")
    else:
        st.error("The uploaded file must contain 'transaction_amount', 'customer_age', and 'customer_balance' columns.")

# Interactive Scatter Plot
st.header("Interactive Scatter Plot")

# Allow users to select columns for X and Y axis
numerical_columns = ['transaction_amount', 'customer_age', 'customer_balance', 'transaction_to_balance_ratio']
x_axis = st.selectbox("Select X-axis", numerical_columns)
y_axis = st.selectbox("Select Y-axis", numerical_columns)

# Plot the scatter plot
if uploaded_file is not None and x_axis and y_axis:
    fig, ax = plt.subplots()
    ax.scatter(df[x_axis], df[y_axis], alpha=0.6)
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(f"Scatter Plot: {x_axis} vs {y_axis}")
    st.pyplot(fig)
