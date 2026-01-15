from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from .schema import LoanApplication, LoanApproval
from .model import predict as model_predict

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the loan pre-screening system", "status": "success"}

@app.post("/predict", response_model=LoanApproval)
def predict(loan_application: LoanApplication):

    data = pd.DataFrame([{
        k: (v.value if hasattr(v, "value") else v)
        for k, v in loan_application.model_dump().items()
    }])

    data = data.drop(columns=["zip_code"], errors="ignore")

    prediction = model_predict(data)

    if int(prediction[0]) == 1:
        return LoanApproval(approval="Congratulations! Your loan has been approved")
    else:
        return LoanApproval(approval="Unfortunately, your loan has been rejected")

