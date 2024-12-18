from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..core.auth import verify_password, create_access_token, get_password_hash, decode_access_token
from ..core.config import settings
from ..db.database import Database

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
db = Database()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": user["email"], "is_admin": user.get("is_admin", False)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/validate")
async def validate_token(token: str = Depends(oauth2_scheme)):
    """Validate access token and return user info"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user = db.get_user_by_email(payload["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
        
    return {
        "email": user["email"],
        "is_admin": user.get("is_admin", False)
    }