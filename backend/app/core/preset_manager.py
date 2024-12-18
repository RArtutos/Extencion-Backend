from typing import List, Dict, Optional
from datetime import datetime
from ..db.database import Database

class PresetManager:
    def __init__(self):
        self.db = Database()

    def create_preset(self, preset_data: Dict) -> Optional[Dict]:
        """Create a new preset"""
        preset_data["created_at"] = datetime.utcnow()
        return self.db.create_preset(preset_data)

    def get_preset(self, preset_id: int) -> Optional[Dict]:
        """Get a specific preset"""
        preset = self.db.get_preset(preset_id)
        if preset:
            preset["user_count"] = len(self.db.get_users_by_preset(preset_id))
        return preset

    def get_all_presets(self) -> List[Dict]:
        """Get all presets with user counts"""
        presets = self.db.get_presets()
        for preset in presets:
            preset["user_count"] = len(self.db.get_users_by_preset(preset["id"]))
        return presets

    def update_preset(self, preset_id: int, preset_data: Dict) -> Optional[Dict]:
        """Update an existing preset"""
        return self.db.update_preset(preset_id, preset_data)

    def delete_preset(self, preset_id: int) -> bool:
        """Delete a preset"""
        return self.db.delete_preset(preset_id)

    def apply_preset_to_user(self, user_id: str, preset_id: int) -> bool:
        """Apply a preset's accounts to a user"""
        preset = self.get_preset(preset_id)
        if not preset:
            return False

        # Remove existing account assignments first
        self.db.user_accounts.remove_all_user_accounts(user_id)

        # Assign new accounts from preset
        success = True
        for account_id in preset.get("account_ids", []):
            if not self.db.assign_account_to_user(user_id, account_id):
                success = False

        return success
