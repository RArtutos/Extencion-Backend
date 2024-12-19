from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SessionBase(BaseModel):
    account_id: int
    domain: Optional[str] = None

class SessionCreate(SessionBase):
    pass

class Session(SessionBase):
    user_id: str
    created_at: datetime
    last_activity: datetime
    active: bool = True