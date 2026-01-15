from pydantic import BaseModel, Field
from enum import Enum

class Gender(str, Enum):
    M = "M"
    F = "F"

class MaritalStatus(str, Enum):
    Married = "Married"
    Single = "Single"
    Divorced = "Divorced"

class Education(str, Enum):
    Bachelors = "Bachelors"
    Masters = "Masters"
    PhD = "PhD"
    HighSchool = "High School"
    Other = "Other"

class Ethnicity(str, Enum):
    Asian = "Asian"
    Black = "Black"
    White = "White"

class BankCustomer(str, Enum):
    Yes = "Yes"
    No = "No"

class PriorDefault(str, Enum):
    Yes = "Yes"
    No = "No"

class Employed(str, Enum):
    Yes = "Yes"
    No = "No"

class DriversLicense(str, Enum):
    Yes = "Yes"
    No = "No"

class Citizen(str, Enum):
    Yes = "Yes"
    No = "No"

class LoanApplication(BaseModel):
    gender: Gender
    age:int = Field(..., description="Age of the applicant")
    debt:float = Field(..., description="Debt of the applicant")
    marital_status: MaritalStatus
    bank_customer: BankCustomer
    education: Education
    ethnicity: Ethnicity
    years_employed:float = Field(..., description="Years employed of the applicant")
    prior_default: PriorDefault
    employed: Employed
    credit_score:int = Field(..., description="Credit score of the applicant")
    drivers_license: DriversLicense
    citizen: Citizen
    zip_code:str = Field(..., description="Zip code of the applicant")
    income:float = Field(..., gt=0, strict=True, description="Income of the applicant")

class LoanApproval(BaseModel):
    approval:str = Field(..., description="Approval of the applicant", examples=["Approved", "Rejected"])