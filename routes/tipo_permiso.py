from fastapi import APIRouter, status
from models.permiso import Permiso
from controllers.permiso import (
    get_all_permisos,
    get_one_permiso,
    create_permiso,
    update_permiso,
    delete_permiso,
)

router = APIRouter(prefix="/permisos/tipo")

@router.get("/", tags=["Permisos"], status_code=status.HTTP_200_OK)
async def list_permisos():
    return await get_all_permisos()

@router.get("/{id}", tags=["Permisos"], status_code=status.HTTP_200_OK)
async def get_permiso(id: int):
    return await get_one_permiso(id)

@router.post("/", tags=["Permisos"], status_code=status.HTTP_201_CREATED)
async def create_new_permiso(permiso: Permiso):
    return await create_permiso(permiso)

@router.put("/", tags=["Permisos"], status_code=status.HTTP_200_OK)
async def update_existing_permiso(permiso: Permiso):
    return await update_permiso(permiso)

@router.delete("/{id}", tags=["Permisos"], status_code=status.HTTP_200_OK)
async def delete_existing_permiso(id: int):
    return await delete_permiso(id)
