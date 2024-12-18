from typing import Dict, List
from datetime import datetime, timedelta
from ..db.analytics import AnalyticsDatabase

class AnalyticsManager:
    def __init__(self):
        self.db = AnalyticsDatabase()

    def get_dashboard_data(self) -> Dict:
        """Get general analytics dashboard data"""
        # Get all accounts first
        accounts = self.db.get_all_accounts()
        
        # Get sessions and users for each account
        accounts_data = []
        for account in accounts:
            sessions = self.db.get_account_sessions(account["id"])
            users = self.db.get_account_users(account["id"])
            accounts_data.append({
                "id": account["id"],
                "name": account["name"],
                "active_sessions": len([s for s in sessions if s.get("active", False)]),
                "total_users": len(users),
                "active_users": len([u for u in users if u.get("is_active", False)])
            })
        
        recent_activity = self.db.get_recent_activities(limit=10)
        
        return {
            "accounts": accounts_data,
            "recent_activity": recent_activity
        }

    def get_user_analytics(self, user_id: str) -> Dict:
        """Get analytics for a specific user"""
        return self.db.get_user_analytics(user_id)

    def get_account_analytics(self, account_id: int) -> Dict:
        """Get analytics for a specific account"""
        sessions = self.db.get_account_sessions(account_id)
        users = self.db.get_account_users(account_id)
        
        return {
            "account_id": account_id,
            "total_users": len(users),
            "active_users": len([u for u in users if u.get("is_active", False)]),
            "total_sessions": len(sessions),
            "current_sessions": len([s for s in sessions if s.get("active", False)]),
            "usage_by_domain": self._aggregate_domain_usage(sessions),
            "user_activities": self.db.get_account_activities(account_id)
        }

    def _aggregate_domain_usage(self, sessions: List[Dict]) -> List[Dict]:
        """Aggregate usage statistics by domain"""
        domain_stats = {}
        for session in sessions:
            domain = session.get("domain")
            if domain:
                if domain not in domain_stats:
                    domain_stats[domain] = {
                        "total_time": 0,
                        "total_sessions": 0
                    }
                domain_stats[domain]["total_sessions"] += 1
                if session.get("duration"):
                    domain_stats[domain]["total_time"] += session["duration"]
        
        return [{"domain": k, **v} for k, v in domain_stats.items()]