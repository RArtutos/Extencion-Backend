from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SessionBase(BaseModel):
    user_id: str
    account_id: int
    last_activity: datetime
    domain: Optional[str] = None

class SessionCreate(SessionBase):
    pass

class Session(SessionBase):
    id: int