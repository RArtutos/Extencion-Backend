from typing import Optional, List, Dict
from .base import Database
from ..core.config import settings

class AccountRepository(Database):
    def __init__(self):
        super().__init__(settings.DATA_FILE)

    def get_accounts(self, user_id: str = None) -> List[Dict]:
        data = self._read_data()
        if user_id:
            user_account_ids = [ua["account_id"] for ua in data.get("user_accounts", []) 
                              if ua["user_id"] == user_id]
            return [acc for acc in data.get("accounts", []) if acc["id"] in user_account_ids]
        return data.get("accounts", [])

    def create_account(self, account_data: Dict) -> Dict:
        data = self._read_data()
        if "accounts" not in data:
            data["accounts"] = []
            
        account_id = max([a.get("id", 0) for a in data["accounts"]], default=0) + 1
        account = {
            "id": account_id,
            **account_data
        }
        
        data["accounts"].append(account)
        self._write_data(data)
        return account

    def get_account(self, account_id: int) -> Optional[Dict]:
        data = self._read_data()
        return next(
            (acc for acc in data.get("accounts", []) if acc["id"] == account_id),
            None
        )

    def update_account(self, account_id: int, account_data: Dict) -> Optional[Dict]:
        data = self._read_data()
        account_index = next(
            (i for i, a in enumerate(data.get("accounts", []))
             if a["id"] == account_id),
            None
        )
        
        if account_index is not None:
            account = data["accounts"][account_index]
            account.update(account_data)
            self._write_data(data)
            return account
        return None

    def delete_account(self, account_id: int) -> bool:
        data = self._read_data()
        initial_count = len(data.get("accounts", []))
        
        data["accounts"] = [
            a for a in data.get("accounts", [])
            if a["id"] != account_id
        ]
        
        data["user_accounts"] = [
            ua for ua in data.get("user_accounts", [])
            if ua["account_id"] != account_id
        ]
        
        if len(data["accounts"]) < initial_count:
            self._write_data(data)
            return True
        return False