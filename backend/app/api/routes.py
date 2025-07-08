# backend/app/api/routes.py
from fastapi import APIRouter, HTTPException
from ..models import SignupModel, KYCModel, InvestorProfileModel, BankLinkRequest
from ..core.security import hash_password

router = APIRouter()
users_db: dict[str, dict] = {}
kyc_db: dict[int, dict] = {}
investor_profiles_db: dict[int, dict] = {}

@router.post("/signup")
def signup(user: SignupModel):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = hash_password(user.password)
    # In a real app, you'd get a user_id from a database
    user_id = len(users_db) + 1
    users_db[user.email] = {
        "id": user_id,
        "email": user.email, 
        "full_name": user.full_name,
        "hashed_password": hashed_pw
    }
    return {"status": "success", "message": "Signup successful", "user_id": user_id}

@router.post("/kyc/submit")
def submit_kyc(kyc: KYCModel):
    # In a real app, you'd verify the user_id exists
    kyc_db[kyc.user_id] = kyc.dict()
    # Mock call to external KYC API
    return {"status": "pending", "message": "KYC submitted, pending verification"}

@router.post("/investor-profile")
def investor_profile(profile: InvestorProfileModel):
    # In a real app, you'd verify the user_id exists
    investor_profiles_db[profile.user_id] = profile.dict()
    return {"status": "success", "message": "Investor profile saved"}

@router.post("/bank-link/initiate")
def initiate_bank_link(data: BankLinkRequest):
    # Mock bank linking flow
    return {"status": "success", "message": "Bank link initiated", "link_url": "https://mock-plaid-link.com/12345"}
