from typing import Optional
from pydantic import BaseModel

class UserAccount(BaseModel):
    user_id: str
    account_id: int
    max_concurrent_users: int = 1
    active_sessions: int = 0
    last_activity: Optional[str] = None