from typing import Optional, Dict
from datetime import datetime
from ..db.database import Database
from ..core.config import settings

class DeviceManager:
    def __init__(self):
        self.db = Database()

    async def verify_device_limit(self, user_id: str, device_info: Dict) -> bool:
        """Verify if user can login from this device"""
        user = self.db.get_user_by_email(user_id)
        if not user:
            return False

        active_sessions = self.db.get_active_sessions(user_id)
        current_device = next(
            (s for s in active_sessions if s["device_id"] == device_info["device_id"]),
            None
        )

        # Allow if it's the same device
        if current_device:
            return True

        # Check against max devices limit
        return len(active_sessions) < user.get("max_devices", 1)

    async def register_device(self, user_id: str, device_info: Dict) -> Optional[str]:
        """Register a new device session"""
        if not await self.verify_device_limit(user_id, device_info):
            return None

        session_id = f"{user_id}_{datetime.utcnow().timestamp()}"
        session_data = {
            "id": session_id,
            "user_id": user_id,
            "device_id": device_info["device_id"],
            "ip_address": device_info["ip_address"],
            "user_agent": device_info["user_agent"],
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow()
        }

        if self.db.create_session(session_data):
            return session_id
        return None