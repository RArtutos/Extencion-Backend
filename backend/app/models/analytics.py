from datetime import datetime
from pydantic import BaseModel

class AccessLog(BaseModel):
    user_id: str
    account_id: int
    domain: str
    timestamp: datetime
    action: str  # 'login', 'logout', 'access'
    ip_address: Optional[str] = None