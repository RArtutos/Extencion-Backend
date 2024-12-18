from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PresetBase(BaseModel):
    name: str
    description: Optional[str] = None
    account_ids: List[int]

class PresetCreate(PresetBase):
    pass

class PresetUpdate(PresetBase):
    pass

class Preset(PresetBase):
    id: int
    created_at: datetime
    user_count: int = 0

    class Config:
        from_attributes = True