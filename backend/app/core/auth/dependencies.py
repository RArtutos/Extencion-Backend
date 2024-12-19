"""Authentication dependencies module"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from ..config import settings
from .token import decode_access_token
from ...db.database import Database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
db = Database()

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get the current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
        
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
        
    user = db.get_user_by_email(email)
    if user is None:
        raise credentials_exception
        
    return user

async def get_current_admin_user(current_user: dict = Depends(get_current_user)):
    """Get the current authenticated admin user"""
    if not current_user.get("is_admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges"
        )
    return current_user