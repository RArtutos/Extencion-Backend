from typing import Optional, Dict, List
from datetime import datetime
from .repositories.user_repository import UserRepository
from .repositories.account_repository import AccountRepository
from .repositories.user_account_repository import UserAccountRepository
from .repositories.preset_repository import PresetRepository
from .repositories.analytics_repository import AnalyticsRepository
from .repositories.session_repository import SessionRepository

class Database:
    def __init__(self):
        self.users = UserRepository()
        self.accounts = AccountRepository()
        self.user_accounts = UserAccountRepository()
        self.presets = PresetRepository()
        self.analytics = AnalyticsRepository()
        self.sessions = SessionRepository()

    # Delegate methods to appropriate repositories
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        return self.users.get_by_email(email)

    def get_users(self) -> List[Dict]:
        return self.users.get_all()

    def create_user(self, user_data: Dict) -> Optional[Dict]:
        return self.users.create(user_data)

    def get_accounts(self, user_id: Optional[str] = None) -> List[Dict]:
        return self.accounts.get_all(user_id)

    def get_account(self, account_id: int) -> Optional[Dict]:
        return self.accounts.get_by_id(account_id)

    def create_account(self, account_data: Dict) -> Optional[Dict]:
        return self.accounts.create(account_data)

    def update_account(self, account_id: int, account_data: Dict) -> Optional[Dict]:
        return self.accounts.update(account_id, account_data)

    def delete_account(self, account_id: int) -> bool:
        return self.accounts.delete(account_id)

    def assign_account_to_user(self, user_id: str, account_id: int) -> bool:
        return self.user_accounts.assign_account(user_id, account_id)

    def remove_account_from_user(self, user_id: str, account_id: int) -> bool:
        return self.user_accounts.remove_account(user_id, account_id)

    def get_user_accounts(self, user_id: str) -> List[int]:
        return self.user_accounts.get_user_accounts(user_id)

    def get_presets(self) -> List[Dict]:
        return self.presets.get_presets()

    def get_preset(self, preset_id: int) -> Optional[Dict]:
        return self.presets.get_preset(preset_id)

    def create_preset(self, preset_data: Dict) -> Optional[Dict]:
        return self.presets.create_preset(preset_data)

    def update_preset(self, preset_id: int, preset_data: Dict) -> Optional[Dict]:
        return self.presets.update_preset(preset_id, preset_data)

    def delete_preset(self, preset_id: int) -> bool:
        return self.presets.delete_preset(preset_id)

    # Session management methods
    def get_active_sessions(self, account_id: int) -> List[Dict]:
        return self.sessions.get_active_sessions(account_id)

    def create_session(self, session_data: Dict) -> bool:
        return self.sessions.create_session(session_data)

    def update_session_activity(self, session_id: str, activity_data: Dict) -> bool:
        return self.sessions.update_session_activity(session_id, activity_data)

    def end_session(self, session_id: str) -> bool:
        return self.sessions.end_session(session_id)

    # User methods
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        return self.users.get_by_email(email)

    def get_users(self) -> List[Dict]:
        return self.users.get_all()

    def create_user(self, user_data: Dict) -> Optional[Dict]:
        return self.users.create(user_data)

    def delete_user(self, user_id: str) -> bool:
        """Delete a user and all their associations"""
        # First remove all account associations
        self.user_accounts.remove_all_user_accounts(user_id)
        # Then delete the user
        return self.users.delete(user_id)

    # Account methods
    def get_accounts(self, user_id: Optional[str] = None) -> List[Dict]:
        return self.accounts.get_all(user_id)

    def get_account(self, account_id: int) -> Optional[Dict]:
        return self.accounts.get_by_id(account_id)

    def assign_account_to_user(self, user_id: str, account_id: int) -> bool:
        return self.user_accounts.assign_account(user_id, account_id)

    def remove_account_from_user(self, user_id: str, account_id: int) -> bool:
        return self.user_accounts.remove_account(user_id, account_id)
