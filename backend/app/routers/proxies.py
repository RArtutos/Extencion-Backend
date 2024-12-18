from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..db.database import Database
from ..schemas.proxy import Proxy, ProxyCreate
from .auth import oauth2_scheme

router = APIRouter()
db = Database()

@router.get("/", response_model=List[Proxy])
async def get_proxies(token: str = Depends(oauth2_scheme)):
    return db.get_proxies()

@router.post("/", response_model=Proxy)
async def create_proxy(proxy: ProxyCreate, token: str = Depends(oauth2_scheme)):
    return db.create_proxy(proxy.dict())

@router.delete("/{proxy_id}")
async def delete_proxy(proxy_id: int, token: str = Depends(oauth2_scheme)):
    if not db.delete_proxy(proxy_id):
        raise HTTPException(status_code=404, detail="Proxy not found")
    return {"message": "Proxy deleted"}