# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from schemas import PHCAccount, PHCLogin
# from database import get_db
# from models import PHCUser
# from hashing import Hash

# router = APIRouter(prefix="/phc", tags=["PHC Authentication"])


# @router.post("/sign-up")
# def create_phc_account(request: PHCAccount, db: Session = Depends(get_db)):
#     existing = db.query(PHCUser).filter(
#         (PHCUser.phc_id == request.phc_id) | (PHCUser.phc_name == request.phc_name)
#     ).first()

#     if existing:
#         raise HTTPException(status_code=400, detail="PHC already registered")

#     new_phc = PHCUser(
#         phc_id=request.phc_id,
#         phc_name=request.phc_name,
#         password=Hash.hashing(request.password)
#     )
#     db.add(new_phc)
#     db.commit()
#     db.refresh(new_phc)
#     return {"message": "PHC account created successfully", "phc_name": new_phc.phc_name}


# @router.post("/sign-in")
# def phc_sign_in(request: PHCLogin, db: Session = Depends(get_db)):
#     phc_user = db.query(PHCUser).filter(PHCUser.phc_id == request.phc_id).first()

#     if not phc_user:
#         raise HTTPException(status_code=404, detail="PHC not found")

#     if not Hash.verifying(request.password, phc_user.password):
#         raise HTTPException(status_code=401, detail="Incorrect password")

#     return {"message": "Login successful", "phc_name": phc_user.phc_name}















from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import os

from database import get_db
from models import PHCUser, HealthAdmin
from schemas import (
    PHCSignupRequest, PHCSignupResponse, PHCLoginRequest, PHCLoginResponse,
    HealthAdminSignupRequest, HealthAdminSignupResponse, HealthAdminLoginRequest, HealthAdminLoginResponse
)

router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "hackhealthsecret")
ALGORITHM = "HS256"

# ---------------- Helper ----------------
def _normalize_role(role: str) -> str:
    if not role:
        return ""
    r = role.strip().lower()
    if r in ("phc", "phcuser", "frontline", "frontline_worker"):
        return "phc"
    if r in ("health", "health_admin", "admin", "healthcare_admin"):
        return "health_admin"
    return r

# ---------------- Signup ----------------
@router.post("/signup")
def signup(request: dict, db: Session = Depends(get_db)):
    """
    Shared signup endpoint for PHC and Health Admins.
    `request` should include 'role' to determine which table to insert into.
    """
    role = _normalize_role(request.get("role", ""))

    if role == "phc":
        data = PHCSignupRequest(**request)
        # Check existing email or PHC name
        existing = db.query(PHCUser).filter(
            (PHCUser.email == data.email) | (PHCUser.phc_name == data.phc_name)
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="PHC already registered")

        new_user = PHCUser(
            phc_name=data.phc_name,
            email=data.email,
            password=pwd_context.hash(data.password[:72]),
            role="phc",
            created_at=datetime.utcnow(),
            capacity=data.capacity,
            consecutive_overload_days=data.consecutive_overload_days,
            latitude=data.latitude,
            longitude=data.longitude
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "PHC user registered successfully!", "phc_name": new_user.phc_name, "role": "phc"}

    elif role == "health_admin":
        data = HealthAdminSignupRequest(**request)
        existing = db.query(HealthAdmin).filter(HealthAdmin.email == data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Health Admin already registered")

        new_user = HealthAdmin(
            full_name=data.full_name,
            email=data.email,
            password=pwd_context.hash(data.password[:72]),
            role="health_admin",
            created_at=datetime.utcnow()
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "Health Admin registered successfully!", "full_name": new_user.full_name, "role": "health_admin"}

    else:
        raise HTTPException(status_code=400, detail="Invalid role. Must be 'phc' or 'health_admin'.")

# ---------------- Login ----------------
@router.post("/login")
def login(request: dict, db: Session = Depends(get_db)):
    """
    Shared login endpoint for PHC and Health Admins.
    Expects email, password, and role in the request.
    """
    role = _normalize_role(request.get("role", ""))
    email = request.get("email", "").strip().lower()
    password = request.get("password", "")

    if role == "phc":
        user = db.query(PHCUser).filter(PHCUser.email == email).first()
        if not user or not pwd_context.verify(password[:72], user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        redirect_to = "/frontline.html"

    elif role == "health_admin":
        user = db.query(HealthAdmin).filter(HealthAdmin.email == email).first()
        if not user or not pwd_context.verify(password[:72], user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        redirect_to = "/admin.html"

    else:
        raise HTTPException(status_code=400, detail="Invalid role")

    # JWT token
    token_data = {"sub": email, "role": role, "exp": datetime.utcnow() + timedelta(hours=12)}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer", "role": role, "redirect_to": redirect_to}
