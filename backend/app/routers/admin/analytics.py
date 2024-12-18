"""Admin analytics routes"""
from fastapi import APIRouter, Depends
from ...core.auth import get_current_admin_user
from ...core.analytics_manager import AnalyticsManager

router = APIRouter()
analytics_manager = AnalyticsManager()

@router.get("/")
async def get_analytics_dashboard(current_user: dict = Depends(get_current_admin_user)):
    """Get general analytics dashboard"""
    return analytics_manager.get_dashboard_data()

@router.get("/user/{user_id}")
async def get_user_analytics(
    user_id: str,
    current_user: dict = Depends(get_current_admin_user)
):
    """Get analytics for a specific user"""
    return analytics_manager.get_user_analytics(user_id)

@router.get("/account/{account_id}")
async def get_account_analytics(
    account_id: int,
    current_user: dict = Depends(get_current_admin_user)
):
    """Get analytics for a specific account"""
    return analytics_manager.get_account_analytics(account_id)