from fastapi import APIRouter, status

from models.permiso import Permiso, ArchivosPermiso, FoldersPermiso
from controllers.permiso import (
    get_all_permisos,
    get_one_permiso,
    create_permiso,
    update_permiso,
    delete_permiso,
    add_permiso_archivo,
    list_permisos_archivo,
    remove_permiso_archivo,
    add_permiso_carpeta,
    list_permisos_carpeta,
    remove_permiso_carpeta,
)

router = APIRouter(prefix="/permisos")

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

# Permisos de Archivo
@router.post("/archivo", tags=["Permisos"], status_code=status.HTTP_201_CREATED)
async def add_permiso_a_archivo(data: ArchivosPermiso):
    return await add_permiso_archivo(data)

@router.get("/archivo/{id_archivo}", tags=["Permisos"], status_code=status.HTTP_200_OK)
async def get_permisos_de_archivo(id_archivo: int):
    return await list_permisos_archivo(id_archivo)

@router.delete("/archivo/{id}", tags=["Permisos"], status_code=status.HTTP_200_OK)
async def remove_permiso_de_archivo(id: int):
    return await remove_permiso_archivo(id)

# Permisos de Carpeta
@router.post("/carpeta", tags=["Permisos"], status_code=status.HTTP_201_CREATED)
async def add_permiso_a_carpeta(data: FoldersPermiso):
    return await add_permiso_carpeta(data)

@router.get("/carpeta/{id_carpeta}", tags=["Permisos"], status_code=status.HTTP_200_OK)
async def get_permisos_de_carpeta(id_carpeta: int):
    return await list_permisos_carpeta(id_carpeta)

@router.delete("/carpeta/{id}", tags=["Permisos"], status_code=status.HTTP_200_OK)
async def remove_permiso_de_carpeta(id: int):
    return await remove_permiso_carpeta(id)