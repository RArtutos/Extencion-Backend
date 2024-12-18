from pydantic import BaseModel
from typing import Optional

class ProxyBase(BaseModel):
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    type: str = "https"  # "https" or "socks5"

class ProxyCreate(ProxyBase):
    pass

class Proxy(ProxyBase):
    id: int