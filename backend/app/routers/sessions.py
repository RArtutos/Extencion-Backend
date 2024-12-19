from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from ..core.auth import get_current_user
from ..db.database import Database
from ..core.analytics_manager import AnalyticsManager

router = APIRouter()
db = Database()
analytics = AnalyticsManager()

@router.get("/{account_id}/status")
async def get_session_status(
    account_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get session status for an account"""
    active_sessions = db.get_active_sessions(account_id)
    account = db.get_account(account_id)
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    current_session = next(
        (s for s in active_sessions if s["user_id"] == current_user["email"]),
        None
    )
    
    return {
        "active_session": bool(current_session),
        "active_sessions": len(active_sessions),
        "max_concurrent_users": account.get("max_concurrent_users", 1)
    }

@router.post("/start")
async def start_session(
    session_data: Dict,
    current_user: dict = Depends(get_current_user)
):
    """Start a new session"""
    account_id = session_data.get("account_id")
    
    # Verificar límites
    active_sessions = db.get_active_sessions(account_id)
    account = db.get_account(account_id)
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if len(active_sessions) >= account.get("max_concurrent_users", 1):
        raise HTTPException(
            status_code=400,
            detail="Maximum concurrent users reached"
        )
    
    # Crear sesión
    success = db.create_session({
        "user_id": current_user["email"],
        "account_id": account_id,
        "domain": session_data.get("domain"),
        "timestamp": session_data.get("timestamp"),
        "active": True
    })
    
    if not success:
        raise HTTPException(
            status_code=400,
            detail="Failed to create session"
        )
    
    return {"message": "Session started successfully"}

@router.put("/{account_id}")
async def update_session(
    account_id: int,
    session_data: Dict,
    current_user: dict = Depends(get_current_user)
):
    """Update session activity"""
    success = db.update_session_activity(
        user_id=current_user["email"],
        account_id=account_id,
        domain=session_data.get("domain")
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"message": "Session updated successfully"}

@router.post("/end")
async def end_session(
    session_data: Dict,
    current_user: dict = Depends(get_current_user)
):
    """End a session"""
    account_id = session_data.get("account_id")
    success = db.end_session(
        user_id=current_user["email"],
        account_id=account_id
    )
    
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"message": "Session ended successfully"}