from fastapi import APIRouter, status
from models.descargas import Descarga
from controllers.descargas import (
    get_downloads_by_user,
    get_downloads_by_file,
    get_one_download,
    create_download,
    update_download,
    delete_download
)

router = APIRouter(prefix="/Descargas")

# Obtener todas las descargas de un usuario
@router.get("/user/{id_usuario}", tags=["Descargas"], status_code=status.HTTP_200_OK)
async def get_all_downloads_by_user(id_usuario: int):
    result = await get_downloads_by_user(id_usuario)
    return result

# Obtener todas las descargas de un archivo
@router.get("/file/{id_archivo}", tags=["Descargas"], status_code=status.HTTP_200_OK)
async def get_all_downloads_by_file(id_archivo: int):
    result = await get_downloads_by_file(id_archivo)
    return result

# Obtener una descarga por ID
@router.get("/{id}", tags=["Descargas"], status_code=status.HTTP_200_OK)
async def get_download_by_id(id: int):
    result = await get_one_download(id)
    return result

# Crear una nueva descarga
@router.post("/", tags=["Descargas"], status_code=status.HTTP_201_CREATED)
async def create_new_download(descarga_data: Descarga):
    result = await create_download(descarga_data)
    return result

# Actualizar una descarga por ID
@router.put("/{id}", tags=["Descargas"], status_code=status.HTTP_200_OK)
async def update_download_by_id(descarga_data: Descarga, id: int):
    descarga_data.id = id
    result = await update_download(descarga_data)
    return result

# Eliminar una descarga por ID
@router.delete("/{id}", tags=["Descargas"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_download_by_id(id: int):
    await delete_download(id)
    return None
