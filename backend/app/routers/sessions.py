from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..db.database import Database
from ..core.auth import get_current_user
from ..schemas.session import SessionCreate, Session

router = APIRouter()
db = Database()

@router.post("/", response_model=Session)
async def create_session(session: SessionCreate, current_user: dict = Depends(get_current_user)):
    """Create a new session"""
    # Verify user has access to the account
    user_accounts = db.get_user_accounts(current_user["email"])
    if session.account_id not in user_accounts:
        raise HTTPException(status_code=403, detail="Not authorized to access this account")
    
    # Check session limits
    account = db.get_account(session.account_id)
    active_sessions = db.get_active_sessions(session.account_id)
    if len(active_sessions) >= account.get("max_concurrent_users", 1):
        raise HTTPException(status_code=400, detail="Maximum concurrent users reached")
    
    session_data = session.dict()
    session_data["user_id"] = current_user["email"]
    
    if db.create_session(session_data):
        return session_data
    raise HTTPException(status_code=400, detail="Failed to create session")

@router.put("/{account_id}")
async def update_session(
    account_id: int,
    session_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Update session activity"""
    # Verify user has access to the account
    user_accounts = db.get_user_accounts(current_user["email"])
    if account_id not in user_accounts:
        raise HTTPException(status_code=403, detail="Not authorized to access this account")
    
    if db.update_session_activity(current_user["email"], account_id, session_data.get("domain")):
        return {"message": "Session updated successfully"}
    raise HTTPException(status_code=400, detail="Failed to update session")

@router.delete("/{account_id}")
async def end_session(account_id: int, current_user: dict = Depends(get_current_user)):
    """End a session"""
    # Verify user has access to the account
    user_accounts = db.get_user_accounts(current_user["email"])
    if account_id not in user_accounts:
        raise HTTPException(status_code=403, detail="Not authorized to access this account")
    
    if db.end_session(current_user["email"], account_id):
        return {"message": "Session ended successfully"}
    raise HTTPException(status_code=400, detail="Failed to end session")