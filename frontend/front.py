import streamlit as st
import requests

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Loan Pre-Screening System",
    page_icon="💳",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/predict"

# ===============================
# SIDEBAR
# ===============================
st.sidebar.title("🏦 Loan AI System")
st.sidebar.markdown("""
**Purpose:** Loan Pre-Screening  
**Model:** Logistic Regression  
**Backend:** FastAPI  
**Frontend:** Streamlit  
""")

st.sidebar.info(
    "This system provides an **instant loan approval prediction** "
    "based on applicant details. Final approval is subject to bank policies."
)

# ===============================
# MAIN HEADER
# ===============================
st.title("💳 Loan Application Portal")
st.caption("AI-powered instant loan pre-screening")

with st.expander("ℹ️ How it works"):
    st.write("""
    1. Enter applicant details  
    2. Data is sent to the ML model via API  
    3. Model evaluates risk  
    4. Instant approval or rejection  
    """)

# ===============================
# FORM
# ===============================
with st.form("loan_form"):
    st.subheader("👤 Personal Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox("Gender", ["M", "F"])
        age = st.number_input("Age", min_value=18, max_value=100)

    with col2:
        marital_status = st.selectbox(
            "Marital Status", ["Married", "Single", "Divorced"]
        )
        ethnicity = st.selectbox(
            "Ethnicity", ["Asian", "Black", "White"]
        )

    with col3:
        citizen = st.selectbox("Citizen", ["Yes", "No"])
        zip_code = st.text_input("Zip Code")

    st.subheader("💼 Employment Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        employed = st.selectbox("Currently Employed", ["Yes", "No"])

    with col2:
        years_employed = st.number_input(
            "Years Employed",
            min_value=0.0,
            max_value=50.0,
            disabled=(employed == "No")
        )

    with col3:
        prior_default = st.selectbox("Prior Loan Default", ["Yes", "No"])

    st.subheader("💰 Financial & Credit Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        income = st.number_input(
            "Annual Income ($)",
            min_value=0,
            step=1000,
            value=40000
        )

    with col2:
        debt = st.number_input(
            "Existing Debt ($)",
            min_value=0.0,
            step=500.0
        )

    with col3:
        credit_score = st.slider(
            "Credit Score",
            min_value=0,
            max_value=1000,
            value=300
        )

    bank_customer = st.selectbox("Existing Bank Customer", ["Yes", "No"])
    education = st.selectbox(
        "Education Level", ["Bachelors", "Masters", "PhD", "High School", "Other"]
    )
    drivers_license = st.selectbox(
        "Driver's License", ["Yes", "No"]
    )

    submitted = st.form_submit_button("🔍 Predict Loan Approval")

# ===============================
# SUBMISSION LOGIC
# ===============================
if submitted:
    if income <= 0:
        st.warning("Income must be greater than zero.")
        st.stop()

    payload = {
        "gender": gender,
        "age": age,
        "debt": debt,
        "marital_status": marital_status,
        "bank_customer": bank_customer,
        "education": education,
        "ethnicity": ethnicity,
        "years_employed": years_employed,
        "prior_default": prior_default,
        "employed": employed,
        "credit_score": credit_score,
        "drivers_license": drivers_license,
        "citizen": citizen,
        "zip_code": zip_code,
        "income": income,
    }

    try:
        with st.spinner("🔍 Evaluating loan application..."):
            response = requests.post(API_URL, json=payload, timeout=10)

        response.raise_for_status()
        result = response.json()

        st.subheader("📊 Prediction Result")

        if "approval" in result:
            approval_text = result["approval"].lower()

            if "approved" in approval_text:
                st.success("✅ Loan Approved")
                st.balloons()
            else:
                st.error("❌ Loan Rejected")

            st.info(result["approval"])
        else:
            st.warning("Unexpected response format from API.")

    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Failed to connect to backend API: {e}")

    except ValueError:
        st.error("🚨 Invalid response received from the API")


