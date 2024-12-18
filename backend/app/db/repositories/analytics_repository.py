from typing import List, Dict, Optional
from datetime import datetime, timedelta
from ..base import BaseRepository
from ...core.config import settings

class AnalyticsRepository(BaseRepository):
    def __init__(self):
        super().__init__(settings.DATA_FILE)

    def get_recent_activities(self, limit: int = 10, account_id: Optional[int] = None) -> List[Dict]:
        data = self._read_data()
        activities = data.get("analytics", [])
        
        # Filter by account if specified
        if account_id is not None:
            activities = [a for a in activities if a.get("account_id") == account_id]
        
        # Sort by timestamp descending and limit
        sorted_activities = sorted(
            activities,
            key=lambda x: x.get("timestamp", ""),
            reverse=True
        )
        return sorted_activities[:limit]

    def get_account_sessions(self, account_id: int) -> List[Dict]:
        data = self._read_data()
        return [
            s for s in data.get("sessions", [])
            if s.get("account_id") == account_id
        ]

    def get_user_sessions(self, user_id: str) -> List[Dict]:
        data = self._read_data()
        return [
            s for s in data.get("sessions", [])
            if s.get("user_id") == user_id
        ]

    def get_account_users(self, account_id: int) -> List[Dict]:
        data = self._read_data()
        user_accounts = [
            ua for ua in data.get("user_accounts", [])
            if ua.get("account_id") == account_id
        ]
        user_ids = [ua.get("user_id") for ua in user_accounts]
        return [
            u for u in data.get("users", [])
            if u.get("email") in user_ids
        ]

    def get_user_account_usage(self, user_id: str) -> List[Dict]:
        data = self._read_data()
        sessions = self.get_user_sessions(user_id)
        
        usage = {}
        for session in sessions:
            account_id = session.get("account_id")
            if account_id not in usage:
                usage[account_id] = {
                    "total_time": 0,
                    "last_access": None
                }
            
            if session.get("duration"):
                usage[account_id]["total_time"] += session["duration"]
            
            timestamp = session.get("last_activity")
            if timestamp:
                current = datetime.fromisoformat(timestamp)
                if not usage[account_id]["last_access"] or current > usage[account_id]["last_access"]:
                    usage[account_id]["last_access"] = current

        # Add account names
        accounts = data.get("accounts", [])
        return [
            {
                "account_id": account_id,
                "name": next((a["name"] for a in accounts if a["id"] == account_id), "Unknown"),
                "total_time": stats["total_time"],
                "last_access": stats["last_access"].isoformat() if stats["last_access"] else None
            }
            for account_id, stats in usage.items()
        ]

    def get_user_total_time(self, user_id: str) -> int:
        sessions = self.get_user_sessions(user_id)
        return sum(s.get("duration", 0) for s in sessions)