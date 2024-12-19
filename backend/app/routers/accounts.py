from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..db.database import Database
from ..schemas.account import Account, AccountCreate
from ..core.auth import get_current_user
from ..core.config import settings

router = APIRouter()
db = Database()

@router.get("/", response_model=List[Account])
async def get_accounts(current_user: dict = Depends(get_current_user)):
    """Get all accounts for the current user"""
    return db.get_accounts(current_user["email"])

@router.get("/{account_id}", response_model=Account)
async def get_account(account_id: int, current_user: dict = Depends(get_current_user)):
    """Get a specific account"""
    account = db.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
        
    # Verify user has access to this account
    user_accounts = db.get_user_accounts(current_user["email"])
    if account["id"] not in user_accounts:
        raise HTTPException(status_code=403, detail="Not authorized to access this account")
        
    return account

@router.get("/{account_id}/session")
async def get_session_info(account_id: int, current_user: dict = Depends(get_current_user)):
    """Get session information for an account"""
    account = db.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
        
    # Verify user has access to this account
    user_accounts = db.get_user_accounts(current_user["email"])
    if account["id"] not in user_accounts:
        raise HTTPException(status_code=403, detail="Not authorized to access this account")
    
    active_sessions = db.get_active_sessions(account_id)
    return {
        "active_sessions": len(active_sessions),
        "max_concurrent_users": account.get("max_concurrent_users", 1)
    }

@router.post("/", response_model=Account)
async def create_account(account: AccountCreate, current_user: dict = Depends(get_current_user)):
    """Create a new account"""
    if not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Not enough privileges")
        
    created_account = db.create_account(account.dict())
    if created_account:
        db.assign_account_to_user(current_user["email"], created_account["id"])
    return created_account

@router.put("/{account_id}", response_model=Account)
async def update_account(account_id: int, account: AccountCreate, current_user: dict = Depends(get_current_user)):
    """Update an existing account"""
    if not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Not enough privileges")
        
    updated_account = db.update_account(account_id, account.dict())
    if not updated_account:
        raise HTTPException(status_code=404, detail="Account not found")
    return updated_account

@router.delete("/{account_id}")
async def delete_account(account_id: int, current_user: dict = Depends(get_current_user)):
    """Delete an account"""
    if not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="Not enough privileges")
        
    if db.delete_account(account_id):
        return {"message": "Account deleted successfully"}
    raise HTTPException(status_code=404, detail="Account not found")