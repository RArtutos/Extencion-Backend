from typing import List, Dict
from ..base import BaseRepository
from ...core.config import settings

class UserAccountRepository(BaseRepository):
    def __init__(self):
        super().__init__(settings.DATA_FILE)

    def assign_account(self, user_id: str, account_id: int) -> bool:
        data = self._read_data()
        if "user_accounts" not in data:
            data["user_accounts"] = []
            
        # Check if assignment already exists
        if any(ua for ua in data["user_accounts"] 
               if ua["user_id"] == user_id and ua["account_id"] == account_id):
            return False
            
        data["user_accounts"].append({
            "user_id": user_id,
            "account_id": account_id
        })
        
        self._write_data(data)
        return True

    def get_user_accounts(self, user_id: str) -> List[int]:
        data = self._read_data()
        return [
            ua["account_id"] for ua in data.get("user_accounts", [])
            if ua["user_id"] == user_id
        ]

    def remove_account(self, user_id: str, account_id: int) -> bool:
        data = self._read_data()
        initial_count = len(data.get("user_accounts", []))
        
        data["user_accounts"] = [
            ua for ua in data.get("user_accounts", [])
            if not (ua["user_id"] == user_id and ua["account_id"] == account_id)
        ]
        
        if len(data["user_accounts"]) < initial_count:
            self._write_data(data)
            return True
        return False

    def remove_all_user_accounts(self, user_id: str) -> bool:
        data = self._read_data()
        initial_count = len(data.get("user_accounts", []))
        
        data["user_accounts"] = [
            ua for ua in data.get("user_accounts", [])
            if ua["user_id"] != user_id
        ]
        
        if len(data["user_accounts"]) < initial_count:
            self._write_data(data)
            return True
        return False