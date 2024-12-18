from datetime import datetime
from typing import Optional, List, Dict
from .base import Database
from ..core.config import settings

class SessionRepository(Database):
    def __init__(self):
        super().__init__(settings.DATA_FILE)

    def create_session(self, session_data: Dict) -> bool:
        data = self._read_data()
        if "sessions" not in data:
            data["sessions"] = []
            
        session_id = max([s.get("id", 0) for s in data["sessions"]], default=0) + 1
        session = {
            "id": session_id,
            **session_data
        }
        
        data["sessions"].append(session)
        self._write_data(data)
        return True

    def update_session_activity(self, user_id: str, account_id: int, domain: Optional[str] = None) -> bool:
        data = self._read_data()
        session = next(
            (s for s in data.get("sessions", []) 
             if s["user_id"] == user_id and s["account_id"] == account_id),
            None
        )
        
        if session:
            session["last_activity"] = datetime.utcnow().isoformat()
            session["domain"] = domain
            self._write_data(data)
            return True
        return False

    def cleanup_inactive_sessions(self, timeout_timestamp: str) -> int:
        data = self._read_data()
        initial_count = len(data.get("sessions", []))
        
        data["sessions"] = [
            s for s in data.get("sessions", [])
            if s["last_activity"] > timeout_timestamp
        ]
        
        self._write_data(data)
        return initial_count - len(data["sessions"])

    def get_active_sessions(self, account_id: int) -> List[Dict]:
        data = self._read_data()
        return [s for s in data.get("sessions", []) if s["account_id"] == account_id]

    def remove_session(self, user_id: str, account_id: int) -> bool:
        data = self._read_data()
        initial_count = len(data.get("sessions", []))
        
        data["sessions"] = [
            s for s in data.get("sessions", [])
            if not (s["user_id"] == user_id and s["account_id"] == account_id)
        ]
        
        if len(data["sessions"]) < initial_count:
            self._write_data(data)
            return True
        return False