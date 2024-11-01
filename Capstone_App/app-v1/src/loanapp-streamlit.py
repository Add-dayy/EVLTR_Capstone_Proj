
import streamlit as st
import requests

st.title("Loan App")

loan_amnt = st.number_input("Loan Amount")
term_numeric = st.number_input("Loan Length (months)")
annual_inc = st.number_input("Annual Income")
emp_title = st.text_input("Employee Title")
emp_length = st.number_input("Length of Employment (months)")

if st.button("Predict"):
    response = requests.post("http://localhost:8502/predict/",
                             json={
                                 "loan_amnt": loan_amnt,
                                 "term_numeric": term_numeric,
                                 "annual_inc": annual_inc
                                 "emp_title": emp_title,
                                 "emp_length": emp_length
                             })
    result = response.json()
    
    if result['fraud_prediction'] == 0:
        st.write("Prediction: Not fraudulent")
    else:
        st.write("Prediction: Fraudulent")


