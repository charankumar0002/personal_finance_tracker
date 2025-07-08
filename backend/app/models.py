# backend/app/models.py
from pydantic import BaseModel, EmailStr
from typing import List

class SignupModel(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class KYCModel(BaseModel):
    user_id: int
    pan_number: str
    aadhaar_number: str
    address: str

class InvestorProfileModel(BaseModel):
    user_id: int
    risk_level: str
    investment_goals: List[str]
    investment_experience: str

class BankLinkRequest(BaseModel):
    user_id: int
