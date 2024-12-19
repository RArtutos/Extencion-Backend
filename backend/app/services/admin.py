"""Admin service module"""
from typing import List, Dict, Optional
from .base_service import BaseService

class AdminService(BaseService):
    def __init__(self):
        super().__init__('/api/admin')

    def create_user(self, user_data: Dict) -> Optional[Dict]:
        """Create a new user and assign preset accounts if specified"""
        preset_id = user_data.get('preset_id')
        
        # Create user first
        user = self._handle_request('post', f"{self.endpoint}/users", user_data)
        
        if user and preset_id:
            # Get preset accounts
            preset = self._handle_request('get', f"{self.endpoint}/presets/{preset_id}")
            if preset and preset.get('account_ids'):
                # Assign each account from the preset
                for account_id in preset['account_ids']:
                    self.assign_account_to_user(user['email'], account_id)
        
        return user