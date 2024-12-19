from typing import Optional, Dict, List
from datetime import datetime
from .repositories.analytics_repository import AnalyticsRepository
from .repositories.account_repository import AccountRepository

class AnalyticsDatabase:
    def __init__(self):
        self.analytics = AnalyticsRepository()
        self.accounts = AccountRepository()

    def get_all_accounts(self) -> List[Dict]:
        """Get all accounts"""
        return self.accounts.get_all()

    def get_recent_activities(self, limit: int = 10) -> List[Dict]:
        return self.analytics.get_recent_activities(limit)

    def get_account_sessions(self, account_id: int) -> List[Dict]:
        return self.analytics.get_account_sessions(account_id)

    def get_user_sessions(self, user_id: str) -> List[Dict]:
        return self.analytics.get_user_sessions(user_id)

    def get_account_users(self, account_id: int) -> List[Dict]:
        return self.analytics.get_account_users(account_id)

    def get_user_account_usage(self, user_id: str) -> List[Dict]:
        return self.analytics.get_user_account_usage(user_id)

    def get_account_activities(self, account_id: int, limit: int = 10) -> List[Dict]:
        """Get recent activities for an account"""
        return self.analytics.get_recent_activities(limit=limit, account_id=account_id)

    def get_user_analytics(self, user_id: str) -> Dict:
        return {
            "user_id": user_id,
            "sessions": self.analytics.get_user_sessions(user_id),
            "account_usage": self.analytics.get_user_account_usage(user_id),
            "total_time": self.analytics.get_user_total_time(user_id),
            "current_sessions": len([s for s in self.analytics.get_user_sessions(user_id) if s.get("active")])
        }