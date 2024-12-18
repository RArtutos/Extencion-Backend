from typing import Optional, List, Dict
from .base import Database
from ..core.config import settings

class PresetRepository(Database):
    def __init__(self):
        super().__init__(settings.DATA_FILE)

    def get_preset(self, preset_id: int) -> Optional[Dict]:
        data = self._read_data()
        return next(
            (p for p in data.get("presets", []) if p["id"] == preset_id),
            None
        )

    def get_presets(self) -> List[Dict]:
        data = self._read_data()
        return data.get("presets", [])

    def create_preset(self, preset_data: dict) -> Optional[dict]:
        data = self._read_data()
        if "presets" not in data:
            data["presets"] = []
            
        preset_id = max([p.get("id", 0) for p in data["presets"]], default=0) + 1
        preset = {
            "id": preset_id,
            **preset_data
        }
        
        data["presets"].append(preset)
        self._write_data(data)
        return preset

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
            return preset
        return None

    def delete_preset(self, preset_id: int) -> bool:
        data = self._read_data()
        initial_count = len(data.get("presets", []))
        
        data["presets"] = [
            p for p in data.get("presets", [])
            if p["id"] != preset_id
        ]
        
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