# Capstone Project - Loan Application Analysis

## Project Overview
This project analyzes loan application data to develop predictive models that assess the likelihood of default. The project uses data from Lending Club and includes data exploration, preprocessing, and modeling steps.

## Directory Structure
- **Capstone_App**: Contains the main application code and data for the project.
  - **app-v1**: Version 1 of the application.
    - **data**: Stores all datasets used in the project.
    - **models**: Saved machine learning models.
    - **notebooks**: Jupyter notebooks for data exploration, processing, and modeling.
    - **src**: Source code for the application.

# Architecture Overview
1. **Data Ingestion**: Raw data is collected and stored in the data directory. The data is initially in CSV format and contains historical loan information.
2. **Data Preprocessing**: Data preprocessing is handled through the notebooks, where data cleaning, transformation, and feature engineering are performed to prepare the data for modeling.
3. **Model Training**: Machine learning models are trained using the cleaned data, with models saved in the models directory. Techniques such as Random Forest and Logistic Regression are used.
4. **Application Layer**: The application is built using Streamlit, allowing users to interactively input data and get predictions on loan defaults.
5. **Deployment**: The application code in the src folder includes Streamlit scripts that can be deployed for real-time scoring.

## Getting Started
1. **Clone the repository**: Use `git clone <repository_url>` to clone this repository.
2. **Run notebooks**: Open Jupyter notebooks in the `notebooks` folder to explore, preprocess, and model the data.
3. **Run the application**: Navigate to the **src** folder and run the Streamlit app using `streamlit run loanapp-streamlit.py`.

## Dependencies
- **Python 3.x**
- **Jupyter Notebook** for EDA and modeling.
- **Streamlit** for building the interactive app.
- **scikit-learn, pandas, numpy** for data processing and modeling.

## Author
- Ade Kolawole


