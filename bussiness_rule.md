# Business Rules Implementation - Complete Guide

## 🎯 Overview

This document explains how **ALL THREE** business rules from `notebooks/04_business_rules.ipynb` are now implemented in production code (`backend/model.py`).

---

## 📋 The Three Business Rules

### **Rule 1: Minimum Credit Score Floor**
```python
if scaled_credit_score < -1.5:
    return REJECTED, "Credit score below minimum threshold"
```

**What it means:**
- Credit scores are **scaled using StandardScaler** 
- A scaled value < -1.5 represents the bottom ~15% of applicants
- This is a **hard regulatory requirement** - no exceptions

**Original credit_score values:**
- Raw values in dataset: 0-17 (discrete ratings, NOT 300-850 FICO)
- 0-2 = Poor → will likely scale to < -1.5 → **REJECTED**
- 3-5 = Fair → borderline
- 6-10 = Good → safe
- 10+ = Excellent → safe

---

### **Rule 2: Debt-to-Income Safety Net**
```python
if scaled_debt > 2.0 AND scaled_income < -0.5:
    return REJECTED, "High debt-to-income ratio"
```

**What it means:**
- BOTH conditions must be true to reject
- `scaled_debt > 2.0` = Debt is 2 standard deviations above average (very high)
- `scaled_income < -0.5` = Income is 0.5 standard deviations below average (low)
- Protects against applicants who can't afford repayment

**Example scenarios:**
- High debt (15.0) + Low income (50.0) → **REJECTED**
- High debt (15.0) + High income (1000.0) → Pass (can afford it)
- Low debt (0.5) + Low income (50.0) → Pass (not risky)

---

### **Rule 3: Prior Default - Anti-Fraud**
```python
if prior_default in ['Yes', 'yes', 'YES', 't', 'T', 1]:
    return REJECTED, "History of prior default"
```

**What it means:**
- **AUTOMATIC REJECTION** - no exceptions
- Any history of prior loan default disqualifies applicant
- Regulatory compliance and fraud prevention
- Overrides even perfect ML predictions

**Accepted values for rejection:**
- String: `"Yes"`, `"yes"`, `"YES"`, `"t"`, `"T"`
- Numeric: `1`
- These handle both encoded (`t`/`f`) and schema (`Yes`/`No`) formats

---

## 🔧 Implementation Details

### **How It Works:**

1. **Data Flow:**
   ```
   Raw Input → pre_process_data() → [Scaled X_num, Encoded X_cat, Original Data]
                                           ↓
   ML Model predicts using scaled/encoded features
                                           ↓
   apply_business_rules() checks SCALED values
                                           ↓
   Return: (final_decision, reason)
   ```

2. **Why We Use Scaled Values:**
   - Business rules in the notebook were designed on scaled data
   - Thresholds (-1.5, 2.0, -0.5) are meaningful in scaled space
   - Ensures consistency with notebook analysis

3. **Feature Order in X_num:**
   ```python
   Index 0: age
   Index 1: debt           ← Used in Rule 2
   Index 2: years_employed
   Index 3: credit_score   ← Used in Rule 1
   Index 4: income         ← Used in Rule 2
   ```

---

## 🧪 Testing Your Implementation

### **Run the Test Suite:**

1. Start your FastAPI server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. In a new terminal, run tests:
   ```bash
   cd backend
   python test_business_rules.py
   ```

### **Expected Results:**

| Test Case | Prior Default | Credit | Debt/Income | Expected Result |
|-----------|--------------|--------|-------------|-----------------|
| Test 1 | **Yes** | 10 (Excellent) | Good | ❌ **REJECTED** (Rule 3) |
| Test 2 | No | 2 (Fair) | **15.0 / 50.0** | ❌ **REJECTED** (Rule 2) |
| Test 3 | No | **0 (Poor)** | Fair | ❌ **REJECTED** (Rule 1) |
| Test 4 | No | 6 (Good) | Good | ✅ **APPROVED** |

---


## ✅ Summary

### **All 3 Rules Now Active:**
1. ✅ **Credit Score Floor** - Protects against poor credit
2. ✅ **Debt-to-Income Ratio** - Protects against unaffordable loans
3. ✅ **Prior Default Check** - Compliance & fraud prevention

### **Why This Matters:**
- **Regulatory Compliance:** Financial institutions MUST enforce hard rules
- **Risk Management:** ML predictions are probabilistic; rules are absolute
- **Transparency:** Clear rejection reasons for auditing
- **Legal Protection:** Documented decision logic

---