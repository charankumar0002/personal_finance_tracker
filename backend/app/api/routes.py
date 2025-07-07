# backend/app/api/routes.py
from fastapi import APIRouter, HTTPException
from ..models import UserCreate
from ..core.security import hash_password

router = APIRouter()
users_db: dict[str, dict] = {}

@router.post("/signup")
def signup(user: UserCreate):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Hash the password before storing
    hashed_pw = hash_password(user.password)
    # Store only email and hashed_password
    users_db[user.email] = {"email": user.email, "hashed_password": hashed_pw}
    return {"msg": "User registered successfully!"}
