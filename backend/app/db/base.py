"""Base repository class with common database operations"""
import json
from typing import Dict
from ..core.utils.json_utils import DateTimeEncoder

class BaseRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _read_data(self) -> dict:
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _write_data(self, data: Dict) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(data, f, cls=DateTimeEncoder, indent=2)