from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ...core.auth import get_current_admin_user
from ...db.database import Database
from ...schemas.account import Account

router = APIRouter()
db = Database()

@router.get("/", response_model=List[Account])
async def get_all_accounts(current_user: dict = Depends(get_current_admin_user)):
    """Get all accounts (admin only)"""
    return db.get_accounts()