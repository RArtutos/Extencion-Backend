from pydantic import BaseModel
from typing import List, Optional

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
    created_at: str