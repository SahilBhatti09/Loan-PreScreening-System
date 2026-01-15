import joblib
import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "model")

# Load models at module level
logistic_model = joblib.load(os.path.join(MODEL_DIR, "logistic_model.pkl"))
random_forest_model = joblib.load(os.path.join(MODEL_DIR, "random_forest_model.pkl"))
encoder = joblib.load(os.path.join(MODEL_DIR, "encoder.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))

def pre_process_data(data: pd.DataFrame):
    categorical_cols = ['gender', 'marital_status', 'bank_customer', 'education', 'ethnicity', 'prior_default', 'employed', 'drivers_license', 'citizen']
    numerical_cols = ['age', 'debt', 'years_employed', 'credit_score', 'income']

    # Keep original data for business rules
    original_data = data.copy()
    data = data.drop(columns=["zip_code"], errors="ignore")

    X_cat = encoder.transform(data[categorical_cols])
    X_num = scaler.transform(data[numerical_cols])

    # Concatenate numerical and categorical features
    X = np.hstack([X_num, X_cat])
    
    return X, X_num, X_cat, original_data

def apply_business_rules(X_num, X_cat, original_data, ml_prediction):
    """
    Apply hard business rules that override ML predictions.
    These rules work on SCALED numerical data and encoded categorical data.
    
    Rules from notebooks/04_business_rules.ipynb:
    1. Minimum Credit Score Floor: credit_score < -1.5 (scaled)
    2. Debt-to-Income Safety Net: debt > 2.0 AND income < -0.5 (scaled)
    3. Prior Default: Automatic rejection for any prior default history
    
    Returns:
        tuple: (final_decision, reason)
    """
    # Extract scaled numerical features (in order: age, debt, years_employed, credit_score, income)
    # Index: 0=age, 1=debt, 2=years_employed, 3=credit_score, 4=income
    scaled_credit_score = X_num[0, 3]
    scaled_debt = X_num[0, 1]
    scaled_income = X_num[0, 4]
    
    # Rule 1: Minimum Credit Score Floor
    # Scaled credit_score below -1.5 means very poor credit
    if scaled_credit_score < -1.5:
        return 0, "Rejected: Credit score below minimum threshold"
    
    # Rule 2: Debt-to-Income Safety Net
    # High scaled debt (>2.0) AND low scaled income (<-0.5)
    if scaled_debt > 2.0 and scaled_income < -0.5:
        return 0, "Rejected: High debt-to-income ratio"
    
    # Rule 3: Anti-Fraud / Prior Default
    # Check original data for prior_default value
    prior_default_value = original_data['prior_default'].values[0]
    if prior_default_value in ['Yes', 'yes', 'YES', 't', 'T', 1]:
        return 0, "Rejected: History of prior default"
    
    # If no hard rules triggered, follow ML prediction
    decision = ml_prediction
    reason = "Approved: Meets all criteria" if decision == 1 else "Rejected: ML Model risk assessment"
    
    return decision, reason

def predict(data: pd.DataFrame):
    X, X_num, X_cat, original_data = pre_process_data(data)
    ml_prediction = logistic_model.predict(X)[0]
    
    # Apply business rules to override ML prediction if necessary
    final_decision, reason = apply_business_rules(X_num, X_cat, original_data, ml_prediction)
    
    # Return as array for consistency
    return np.array([final_decision])
