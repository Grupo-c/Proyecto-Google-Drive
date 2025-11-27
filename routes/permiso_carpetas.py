from fastapi import APIRouter, status
from models.permiso_carpeta import FoldersPermiso
from controllers.permiso_carpetas import (
    add_permiso_carpeta,
    list_permisos_carpeta,
    remove_permiso_carpeta,
)

router = APIRouter(prefix="/permisos/carpeta")

@router.post("/", tags=["Permisos"], status_code=status.HTTP_201_CREATED)
async def add_permiso_a_carpeta(data: FoldersPermiso):
    return await add_permiso_carpeta(data)

@router.get("/{id_carpeta}", tags=["Permisos"], status_code=status.HTTP_200_OK)
async def get_permisos_de_carpeta(id_carpeta: int):
    return await list_permisos_carpeta(id_carpeta)

@router.delete("/{id}", tags=["Permisos"], status_code=status.HTTP_200_OK)
async def remove_permiso_de_carpeta(id: int):
    return await remove_permiso_carpeta(id)
