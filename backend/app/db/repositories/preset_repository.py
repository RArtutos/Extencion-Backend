from typing import Optional, List, Dict
from datetime import datetime
from ..base import BaseRepository
from ...core.config import settings
from ...core.utils.date_utils import parse_datetime, format_datetime

class PresetRepository(BaseRepository):
    def __init__(self):
        super().__init__(settings.DATA_FILE)

    def _process_preset(self, preset: Dict, users: List[Dict]) -> Dict:
        """Process a preset dictionary to ensure proper data format"""
        processed = preset.copy()
        
        # Add user count
        processed["user_count"] = len([
            user for user in users
            if user.get("preset_id") == preset["id"]
        ])
        
        # Handle created_at datetime
        if isinstance(processed.get("created_at"), str):
            processed["created_at"] = parse_datetime(processed["created_at"])
            
        return processed

    def get_presets(self) -> List[Dict]:
        data = self._read_data()
        users = data.get("users", [])
        presets = data.get("presets", [])
        
        return [self._process_preset(preset, users) for preset in presets]

    def get_preset(self, preset_id: int) -> Optional[Dict]:
        data = self._read_data()
        preset = next(
            (p for p in data.get("presets", []) if p["id"] == preset_id),
            None
        )
        
        if preset:
            return self._process_preset(preset, data.get("users", []))
        return None

    def create_preset(self, preset_data: dict) -> Optional[dict]:
        data = self._read_data()
        if "presets" not in data:
            data["presets"] = []
            
        preset_id = max([p.get("id", 0) for p in data["presets"]], default=0) + 1
        preset = {
            "id": preset_id,
            "created_at": datetime.utcnow(),
            **preset_data,
            "user_count": 0
        }
        
        data["presets"].append(preset)
        self._write_data(data)
        return self._process_preset(preset, data.get("users", []))

    def update_preset(self, preset_id: int, preset_data: dict) -> Optional[dict]:
        data = self._read_data()
        preset_index = next(
            (i for i, p in enumerate(data.get("presets", []))
             if p["id"] == preset_id),
            None
        )
        
        if preset_index is not None:
            preset = data["presets"][preset_index]
            preset.update(preset_data)
            self._write_data(data)
            return self._process_preset(preset, data.get("users", []))
        return None

    def delete_preset(self, preset_id: int) -> bool:
        data = self._read_data()
        initial_count = len(data.get("presets", []))
        
        data["presets"] = [
            p for p in data.get("presets", [])
            if p["id"] != preset_id
        ]
        
        # Update users that were using this preset
        for user in data.get("users", []):
            if user.get("preset_id") == preset_id:
                user["preset_id"] = None
        
        if len(data["presets"]) < initial_count:
            self._write_data(data)
            return True
        return False

    def get_users_by_preset(self, preset_id: int) -> List[dict]:
        data = self._read_data()
        return [
            user for user in data.get("users", [])
            if user.get("preset_id") == preset_id
        ]