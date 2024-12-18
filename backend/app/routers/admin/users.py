from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ...core.auth import get_current_admin_user
from ...db.database import Database
from ...schemas.user import UserCreate, UserResponse

router = APIRouter()
db = Database()

@router.get("/", response_model=List[UserResponse])
async def get_users(current_user: dict = Depends(get_current_admin_user)):
    users = db.get_users()
    return users

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, current_user: dict = Depends(get_current_admin_user)):
    if db.get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return db.create_user(user.dict())

@router.delete("/{user_id}")
async def delete_user(user_id: str, current_user: dict = Depends(get_current_admin_user)):
    """Delete a user"""
    if user_id == current_user["email"]:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    if db.get_user_by_email(user_id).get("is_admin"):
        raise HTTPException(status_code=400, detail="Cannot delete admin users")
        
    if db.delete_user(user_id):
        return {"success": True, "message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/{user_id}/accounts")
async def get_user_accounts(user_id: str, current_user: dict = Depends(get_current_admin_user)):
    """Get accounts assigned to a user"""
    user = db.get_user_by_email(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return db.get_accounts(user_id)

@router.post("/{user_id}/accounts/{account_id}")
async def assign_account(
    user_id: str, 
    account_id: int, 
    current_user: dict = Depends(get_current_admin_user)
):
    """Assign account to user"""
    user = db.get_user_by_email(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    account = db.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
        
    if db.assign_account_to_user(user_id, account_id):
        return {"success": True, "message": "Account assigned successfully"}
    raise HTTPException(status_code=400, detail="Failed to assign account")

@router.delete("/{user_id}/accounts/{account_id}")
async def remove_account(
    user_id: str, 
    account_id: int, 
    current_user: dict = Depends(get_current_admin_user)
):
    """Remove account from user"""
    user = db.get_user_by_email(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    account = db.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
        
    if db.remove_account_from_user(user_id, account_id):
        return {"success": True, "message": "Account removed successfully"}
    raise HTTPException(status_code=400, detail="Failed to remove account")