from fastapi import APIRouter, status

from models.archivo import Archivo,ArchivoUpdate
from controllers.archivo import (
    create_file,
    update_file,
    delete_file,
    get_all_files,
    get_one_file
)

router = APIRouter(prefix="/archivos")


@router.get("/", tags=["Archivos"], status_code=status.HTTP_200_OK)
async def get_all_archivos():
    result = await get_all_files()
    return result


@router.post("/", tags=["Archivos"], status_code=status.HTTP_201_CREATED)
async def create_new_archivo(archivo_data: Archivo):
    result = await create_file(archivo_data)
    return result


@router.put("/{id}", tags=["Archivos"], status_code=status.HTTP_200_OK)
async def update_archivo_info(id: int, archivo_data: ArchivoUpdate):
    archivo_data.id = id  
    result = await update_file(archivo_data)
    return result


@router.delete("/{id}", tags=["Archivos"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_archivo(id: int):
    status_message = await delete_file(id)
    return status_message


@router.get("/{id}", tags=["Archivos"], status_code=status.HTTP_200_OK)
async def get_one_archivo(id: int):
    result = await get_one_file(id)
    return result
