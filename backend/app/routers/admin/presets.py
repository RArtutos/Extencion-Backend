from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ...db.database import Database
from ...core.auth import get_current_admin_user
from ...schemas.preset import PresetCreate, PresetUpdate, Preset

router = APIRouter()
db = Database()

@router.get("/", response_model=List[Preset])
async def get_presets(current_user: dict = Depends(get_current_admin_user)):
    return db.get_presets()

@router.post("/", response_model=Preset)
async def create_preset(preset: PresetCreate, current_user: dict = Depends(get_current_admin_user)):
    return db.create_preset(preset.dict())

@router.get("/{preset_id}", response_model=Preset)
async def get_preset(preset_id: int, current_user: dict = Depends(get_current_admin_user)):
    preset = db.get_preset(preset_id)
    if not preset:
        raise HTTPException(status_code=404, detail="Preset not found")
    return preset

@router.put("/{preset_id}", response_model=Preset)
async def update_preset(
    preset_id: int,
    preset: PresetUpdate,
    current_user: dict = Depends(get_current_admin_user)
):
    updated_preset = db.update_preset(preset_id, preset.dict())
    if not updated_preset:
        raise HTTPException(status_code=404, detail="Preset not found")
    return updated_preset

@router.delete("/{preset_id}")
async def delete_preset(preset_id: int, current_user: dict = Depends(get_current_admin_user)):
    if not db.delete_preset(preset_id):
        raise HTTPException(status_code=404, detail="Preset not found")
    return {"message": "Preset deleted successfully"}