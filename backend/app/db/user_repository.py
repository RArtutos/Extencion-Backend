from datetime import datetime, timedelta
from typing import Optional, List, Dict
from .base import Database
from ..core.auth import get_password_hash
from ..core.config import settings

class UserRepository(Database):
    def __init__(self):
        super().__init__(settings.DATA_FILE)

    def get_users(self) -> List[Dict]:
        data = self._read_data()
        users = data.get("users", [])
        
        for user in users:
            if isinstance(user.get("created_at"), str):
                user["created_at"] = datetime.fromisoformat(user["created_at"])
            if user.get("expires_at") and isinstance(user["expires_at"], str):
                user["expires_at"] = datetime.fromisoformat(user["expires_at"])
            
            user["is_active"] = True
            if user.get("expires_at"):
                user["is_active"] = datetime.utcnow() < user["expires_at"]
            
            user["assigned_accounts"] = [
                ua["account_id"] for ua in data.get("user_accounts", [])
                if ua["user_id"] == user["email"]
            ]
        
        return users

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        data = self._read_data()
        user = next((user for user in data["users"] if user["email"] == email), None)
        
        if user:
            if user.get("expires_at"):
                expires_at = datetime.fromisoformat(user["expires_at"])
                if datetime.utcnow() > expires_at:
                    return None
                    
            user["assigned_accounts"] = [
                ua["account_id"] for ua in data["user_accounts"] 
                if ua["user_id"] == email
            ]
        return user

    def create_user(self, email: str, password: str, is_admin: bool = False, 
                   expires_in_days: Optional[int] = None, preset_id: Optional[int] = None) -> Dict:
        data = self._read_data()
        
        expires_at = None
        if expires_in_days is not None:
            expires_at = (datetime.utcnow() + timedelta(days=expires_in_days)).isoformat()

        user = {
            "email": email,
            "password": get_password_hash(password),
            "is_admin": is_admin,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": expires_at,
            "preset_id": preset_id,
            "assigned_accounts": []
        }
        
        data["users"].append(user)
        self._write_data(data)
        return user