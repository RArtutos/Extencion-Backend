from datetime import datetime
from typing import List, Dict, Optional
from ..base import BaseRepository
from ...core.config import settings

class SessionRepository(BaseRepository):
    def __init__(self):
        super().__init__(settings.DATA_FILE)

    def get_active_sessions(self, account_id: int) -> List[Dict]:
        """Get all active sessions for an account"""
        data = self._read_data()
        sessions = data.get("sessions", [])
        
        # Filter active sessions for the account
        active_sessions = [
            session for session in sessions
            if session.get("account_id") == account_id and
            session.get("active", True) and
            self._is_session_active(session)
        ]
        
        return active_sessions

    def create_session(self, session_data: Dict) -> bool:
        """Create a new session"""
        data = self._read_data()
        if "sessions" not in data:
            data["sessions"] = []
            
        session_data["created_at"] = datetime.utcnow().isoformat()
        session_data["last_activity"] = datetime.utcnow().isoformat()
        session_data["active"] = True
        
        # Verificar límites de sesiones activas
        active_sessions = self.get_active_sessions(session_data["account_id"])
        account = next(
            (a for a in data.get("accounts", []) 
             if a["id"] == session_data["account_id"]),
            None
        )
        
        if account and len(active_sessions) >= account.get("max_concurrent_users", 1):
            return False
            
        data["sessions"].append(session_data)
        self._write_data(data)
        
        # Actualizar analytics
        self._update_analytics(data, session_data, "session_start")
        return True

    def update_session_activity(self, session_id: str, activity_data: Dict) -> bool:
        """Update session activity"""
        data = self._read_data()
        session = next(
            (s for s in data.get("sessions", []) if s.get("id") == session_id),
            None
        )
        
        if session:
            session.update(activity_data)
            session["last_activity"] = datetime.utcnow().isoformat()
            self._write_data(data)
            
            # Actualizar analytics
            self._update_analytics(data, session, "session_activity")
            return True
        return False

    def end_session(self, session_id: str) -> bool:
        """End a session"""
        data = self._read_data()
        session = next(
            (s for s in data.get("sessions", []) if s.get("id") == session_id),
            None
        )
        
        if session:
            session["active"] = False
            session["end_time"] = datetime.utcnow().isoformat()
            if session.get("created_at"):
                start = datetime.fromisoformat(session["created_at"])
                end = datetime.utcnow()
                session["duration"] = (end - start).total_seconds()
            
            self._write_data(data)
            
            # Actualizar analytics
            self._update_analytics(data, session, "session_end")
            return True
        return False

    def _update_analytics(self, data: Dict, session: Dict, event_type: str):
        """Update analytics data"""
        if "analytics" not in data:
            data["analytics"] = []
            
        analytics_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "account_id": session["account_id"],
            "user_id": session["user_id"],
            "session_id": session["id"],
            "domain": session.get("domain"),
            "duration": session.get("duration")
        }
        
        data["analytics"].append(analytics_entry)
        self._write_data(data)

    def _is_session_active(self, session: Dict) -> bool:
        """Check if a session is still active based on last activity"""
        if not session.get("last_activity"):
            return False
            
        last_activity = datetime.fromisoformat(session["last_activity"])
        timeout = datetime.utcnow() - settings.COOKIE_INACTIVITY_TIMEOUT
        return last_activity > timeout