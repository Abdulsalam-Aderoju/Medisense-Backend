from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from database import get_db
from models import User
from schemas import UserSignup, UserLogin, TokenResponse
from jwt_handler import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(prefix="/auth", tags=["Auth"])

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)



@router.post("/signup", response_model=TokenResponse)
def signup(user: UserSignup, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(400, "Email already exists")
    
    if user.role == "phc" and not user.phc_id:
        raise HTTPException(
            status_code=400, 
            detail="PHC ID is required when registering a Primary Health Centre account."
        )

    new_user = User(
        full_name = user.name,                    # ← facility name goes here
        email     = user.email,
        password_hash = hash_password(user.password),
        role      = user.role,
        phc_id    = user.phc_id,
        phc_name  = user.name if user.role == "phc" else None,
        lga_id    = user.lga_id,
    )
    db.add(new_user); db.commit(); db.refresh(new_user)

    access_token = create_access_token({
        "user_id": new_user.id,
        "role": new_user.role,
        "operator_name": user.name,               
        "name": user.name,                       
        "phc_id": new_user.phc_id,
        "lga_id": new_user.lga_id,
    })
    return TokenResponse(access_token=access_token, role = new_user.role)


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    access_token = create_access_token({
        "user_id": db_user.id,
        "role": db_user.role,
        "operator_name": user.operator_name,  
        "name": db_user.full_name,              
        "phc_id": db_user.phc_id,
        "lga_id": db_user.lga_id,
    })
    return TokenResponse(access_token=access_token, role = db_user.role)


@router.post("/token", response_model=TokenResponse)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # Swagger sends 'username' and 'password'. 
    # We map 'username' to your 'email' field.
    db_user = db.query(User).filter(User.email == form_data.username).first()
    
    if not db_user or not verify_password(form_data.password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate the token
    # Note: Swagger UI doesn't send "operator_name", so we use a placeholder or the user's name
    access_token = create_access_token({
        "user_id": db_user.id,
        "role": db_user.role,
        "operator_name": "SwaggerAdmin",  # Placeholder since Swagger can't send this
        "name": db_user.full_name,
        "phc_id": db_user.phc_id,
        "lga_id": db_user.lga_id,
    })
    
    return TokenResponse(access_token=access_token, role = db_user.role)