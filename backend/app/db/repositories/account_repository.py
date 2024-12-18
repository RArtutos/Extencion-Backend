from typing import List, Dict, Optional
from ..base import BaseRepository
from ...core.config import settings

class AccountRepository(BaseRepository):
    def __init__(self):
        super().__init__(settings.DATA_FILE)

    def get_all(self, user_id: Optional[str] = None) -> List[Dict]:
        data = self._read_data()
        accounts = data.get("accounts", [])
        
        # Filter by user if specified
        if user_id:
            user_account_ids = [
                ua["account_id"] for ua in data.get("user_accounts", []) 
                if ua["user_id"] == user_id
            ]
            accounts = [acc for acc in accounts if acc["id"] in user_account_ids]
        
        # Ensure max_concurrent_users is set
        for account in accounts:
            if "max_concurrent_users" not in account:
                account["max_concurrent_users"] = 1
            
        return accounts

    def get_by_id(self, account_id: int) -> Optional[Dict]:
        data = self._read_data()
        account = next(
            (acc for acc in data.get("accounts", []) if acc["id"] == account_id),
            None
        )
        
        if account and "max_concurrent_users" not in account:
            account["max_concurrent_users"] = 1
            
        return account

    def create(self, account_data: Dict) -> Dict:
        data = self._read_data()
        if "accounts" not in data:
            data["accounts"] = []
            
        account_id = max([a.get("id", 0) for a in data["accounts"]], default=0) + 1
        
        # Ensure max_concurrent_users is set
        if "max_concurrent_users" not in account_data:
            account_data["max_concurrent_users"] = 1
            
        account = {
            "id": account_id,
            **account_data
        }
        
        data["accounts"].append(account)
        self._write_data(data)
        return account

    def update(self, account_id: int, account_data: Dict) -> Optional[Dict]:
        data = self._read_data()
        account_index = next(
            (i for i, a in enumerate(data.get("accounts", []))
             if a["id"] == account_id),
            None
        )
        
        if account_index is not None:
            account = data["accounts"][account_index]
            
            # Preserve max_concurrent_users if not provided
            if "max_concurrent_users" not in account_data:
                account_data["max_concurrent_users"] = account.get("max_concurrent_users", 1)
                
            account.update(account_data)
            self._write_data(data)
            return account
        return None