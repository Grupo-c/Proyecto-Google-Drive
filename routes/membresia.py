from fastapi import APIRouter, status
from models.membresia import Membresia
from controllers.membresia import (
    get_all_membresias,
    get_one_membresia,
    create_membresia,
    update_membresia,
    delete_membresia
)

router = APIRouter(prefix="/membresias")

@router.get("/", tags=["Membresías"], status_code=status.HTTP_200_OK)
async def all_membresias():
    return await get_all_membresias()

@router.get("/{id}", tags=["Membresías"])
async def one_membresia(id: int):
    return await get_one_membresia(id)

@router.post("/", tags=["Membresías"], status_code=status.HTTP_201_CREATED)
async def new_membresia(data: Membresia):
    return await create_membresia(data)

@router.put("/{id}", tags=["Membresías"])
async def update_memb(id: int, data: Membresia):
    return await update_membresia(id, data)

@router.delete("/{id}", tags=["Membresías"])
async def delete_memb(id: int):
    return await delete_membresia(id)
