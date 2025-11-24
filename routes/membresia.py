from fastapi import APIRouter, status
from models.membresia import Membresia
from controllers.membresia import get_one_membership as get_membership_controller

router = APIRouter(prefix="/membresias")

@router.get("/{id}", tags=["Membresia"], status_code=status.HTTP_200_OK)
async def get_membership(id: int):
    result = await get_membership_controller(id)
    return result
