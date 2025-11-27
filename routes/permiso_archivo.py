from fastapi import APIRouter, status
from models.permiso_archivo import ArchivosPermiso
from controllers.permiso_archivo import (
    add_permiso_archivo,
    list_permisos_archivo,
    remove_permiso_archivo,
)

router = APIRouter(prefix="/permisos/archivo")

@router.post("/", tags=["Permisos"], status_code=status.HTTP_201_CREATED)
async def add_permiso_a_archivo(data: ArchivosPermiso):
    return await add_permiso_archivo(data)

@router.get("/{id_archivo}", tags=["Permisos"], status_code=status.HTTP_200_OK)
async def get_permisos_de_archivo(id_archivo: int):
    return await list_permisos_archivo(id_archivo)

@router.delete("/{id}", tags=["Permisos"], status_code=status.HTTP_200_OK)
async def remove_permiso_de_archivo(id: int):
    return await remove_permiso_archivo(id)
