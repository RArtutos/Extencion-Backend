from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..db.database import Database
from ..core.auth import get_current_admin_user
from ..schemas.user import UserCreate, UserResponse
from ..schemas.preset import PresetCreate, PresetUpdate, Preset
from ..core.analytics_manager import AnalyticsManager

router = APIRouter()
db = Database()
analytics_manager = AnalyticsManager()

@router.get("/users", response_model=List[UserResponse])
async def get_users(current_user: dict = Depends(get_current_admin_user)):
    return db.get_users()

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, current_user: dict = Depends(get_current_admin_user)):
    if db.get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return db.create_user(
        user.email, 
        user.password, 
        user.is_admin,
        expires_in_days=user.expires_in_days,
        preset_id=user.preset_id
    )

@router.get("/users/{user_id}/accounts")
async def get_user_accounts(user_id: str, current_user: dict = Depends(get_current_admin_user)):
    user = db.get_user_by_email(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return db.get_accounts(user_id)

@router.get("/analytics")
async def get_analytics_dashboard(current_user: dict = Depends(get_current_admin_user)):
    """Get general analytics dashboard"""
    return analytics_manager.get_dashboard_data()

@router.get("/analytics/user/{user_id}")
async def get_user_analytics(
    user_id: str,
    current_user: dict = Depends(get_current_admin_user)
):
    """Get analytics for a specific user"""
    return analytics_manager.get_user_analytics(user_id)

@router.get("/analytics/account/{account_id}")
async def get_account_analytics(
    account_id: int,
    current_user: dict = Depends(get_current_admin_user)
):
    """Get analytics for a specific account"""
    return analytics_manager.get_account_analytics(account_id)