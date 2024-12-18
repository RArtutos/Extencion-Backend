from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AccountActivity(BaseModel):
    account_id: int
    user_id: str
    action: str  # 'login', 'logout', 'access'
    timestamp: datetime
    ip_address: Optional[str]
    user_agent: Optional[str]
    domain: Optional[str]

class UserAnalytics(BaseModel):
    user_id: str
    total_time: int  # Total time in seconds
    total_sessions: int
    current_sessions: int
    last_activity: Optional[datetime]
    account_usage: List[dict]

class AccountAnalytics(BaseModel):
    account_id: int
    total_users: int
    active_users: int
    total_sessions: int
    current_sessions: int
    usage_by_domain: List[dict]
    user_activities: List[AccountActivity]