# backend/app/api/routes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..models import SignupModel, KYCModel, InvestorProfileModel, BankLinkRequest
from ..core.security import hash_password
from ..dependencies import get_db
from ..db.models import User

router = APIRouter()

@router.post("/signup")
def signup(user: SignupModel, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(user.password)
    db_user = User(email=user.email, full_name=user.full_name, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"status": "success", "message": "Signup successful", "user_id": db_user.id}

@router.post("/kyc/submit")
def submit_kyc(kyc: KYCModel, db: Session = Depends(get_db)):
    from ..db.models import KYC, User
    user = db.query(User).filter(User.id == kyc.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    existing_kyc = db.query(KYC).filter(KYC.user_id == kyc.user_id).first()
    if existing_kyc:
        raise HTTPException(status_code=400, detail="KYC already submitted")
    kyc_obj = KYC(
        user_id=kyc.user_id,
        pan_number=kyc.pan_number,
        aadhaar_number=kyc.aadhaar_number,
        address=kyc.address
    )
    db.add(kyc_obj)
    db.commit()
    db.refresh(kyc_obj)
    return {"status": "pending", "message": "KYC submitted, pending verification"}

@router.post("/investor-profile")
def investor_profile(profile: InvestorProfileModel, db: Session = Depends(get_db)):
    from ..db.models import InvestorProfile, User
    user = db.query(User).filter(User.id == profile.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    existing_profile = db.query(InvestorProfile).filter(InvestorProfile.user_id == profile.user_id).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Investor profile already exists")
    profile_obj = InvestorProfile(
        user_id=profile.user_id,
        risk_level=profile.risk_level,
        investment_goals=','.join(profile.investment_goals),
        investment_experience=profile.investment_experience
    )
    db.add(profile_obj)
    db.commit()
    db.refresh(profile_obj)
    return {"status": "success", "message": "Investor profile saved"}

@router.post("/bank-link/initiate")
def initiate_bank_link(data: BankLinkRequest, db: Session = Depends(get_db)):
    from ..db.models import User
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Mock bank linking flow
    return {"status": "success", "message": "Bank link initiated", "link_url": "https://mock-plaid-link.com/12345"}
