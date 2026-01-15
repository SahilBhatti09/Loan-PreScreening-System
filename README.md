# 🏦 Loan Application Pre-Screening System

A real-world, end-to-end Machine Learning project that simulates how banks pre-screen loan applications using **ML models + business rules**.

This project is designed to be **industry-aligned**, and easy to understand for both technical and non-technical stakeholders.

---

## 📌 Problem Statement

Banks receive thousands of loan applications daily.  
Manual screening is slow, inconsistent, and risky.

**Goal:**  
Build a system that:
- Predicts loan approval using Machine Learning
- Applies business rules to reduce risk
- Explains decisions clearly

---

## 🧠 Solution Overview

This project follows a **real ML system pipeline**, not just a model:

Raw Data → Preprocessing → Model → Business Rules → Final Decisions → Evaluation


Key highlights:
- ML handles patterns
- Business rules handle risk & compliance
- Final output is explainable and actionable

---

## 🗂 Project Structure

Loan-PreScreening-System/
│
├── data/
│   ├── raw/
│   │   └── loan_data.csv
│   └── processed/
│       ├── train_data.csv
│       └── test_data.csv
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_model_training.ipynb
│   ├── 04_business_rules.ipynb
│   └── 05_final_evaluation.ipynb
│
├── backend/           
│   ├── main.py
│   ├── model.py
│   └── schema.py
│
├── frontend/          
│   └── front.py
│
├── model/             
│   ├── logistic_model.pkl
│   ├── random_forest_model.pkl
│   ├── encoder.pkl
│   └── scaler.pkl
│
├── src/
│   ├── preprocessing.py
│   ├── train_model.py
│   ├── business_rules.py
│   └── explainability.py
│
├── results/           # Evaluation results only
│   ├── final_evaluation_report.csv
│   └── loan_decisions_with_rules.csv
│
├── README.md
├── bussiness_rule.md
└── requirements.txt


---

## 📘 Notebook Breakdown

### 1️⃣ Data Exploration
- Understand raw data
- Identify missing values & data types
- Explore target distribution

### 2️⃣ Preprocessing
- Column renaming
- Handling missing values
- Encoding categorical features
- Scaling numerical features
- Train-test split
- Save clean dataset

### 3️⃣ Model Training
- Logistic Regression model
- Baseline ML evaluation
- Precision, recall, confusion matrix
- Model validation (no business logic yet)

### 4️⃣ Business Rules
Business rules override model decisions when needed:
- Low income → Reject
- High debt → Reject
- Bad credit history → Reject

This reflects **real banking systems**.

### 5️⃣ Final Evaluation
- Evaluate final decisions (model + rules)
- Classification report
- Confusion matrix
- Final approval/rejection outcomes
- Export results to CSV

---

## 🧪 Technologies Used

**Machine Learning & Data Science:**
- Python 3.12+
- Pandas, NumPy
- Scikit-learn
- Matplotlib, Seaborn
- Jupyter Notebook

**Backend:**
- FastAPI
- Pydantic
- Uvicorn

**Frontend:**
- Streamlit
- Requests

---

## 🚀 How to Run

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Start the Backend API

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://127.0.0.1:8000`

### 3️⃣ Start the Frontend (New Terminal)

```bash
streamlit run frontend/front.py
```

The app will open automatically in your browser at `http://localhost:8501`

### 4️⃣ Test the System

1. Fill in the loan application form
2. Click "Predict Loan Approval"
3. View instant approval/rejection decision

---

## 🚀 Why This Project Matters

✔ **Full-stack ML application** with API and UI  
✔ Realistic ML workflow following industry standards  
✔ Business-aligned logic with rule-based overrides  
✔ Clear separation of concerns (backend/frontend/models)  
✔ Explainable decisions for stakeholders  
✔ Production-ready architecture  
✔ Resume & interview ready  

---

## 👤 Author
Sahil Bhatti