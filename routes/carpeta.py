from fastapi import APIRouter, status
from models.carpeta import Carpeta
from controllers.carpeta import (
    create_carpeta,
    update_carpeta,
    delete_carpeta,
    get_all_carpetas,
    get_one_carpeta
)

router = APIRouter(prefix="/carpetas")

@router.get("/", tags=["Carpetas"], status_code=status.HTTP_200_OK)
async def get_all_carpetas_route():
    return await get_all_carpetas()

@router.post("/", tags=["Carpetas"], status_code=status.HTTP_201_CREATED)
async def create_new_carpeta(carpeta_data: Carpeta):
    return await create_carpeta(carpeta_data)

@router.put("/{id}", tags=["Carpetas"], status_code=status.HTTP_201_CREATED)
async def update_carpeta_route(carpeta_data: Carpeta, id: int):
    carpeta_data.id = id
    return await update_carpeta(carpeta_data)

@router.delete("/{id}", tags=["Carpetas"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_carpeta_route(id: int):
    return await delete_carpeta(id)

@router.get("/{id}", tags=["Carpetas"], status_code=status.HTTP_200_OK)
async def get_one_carpeta_route(id: int):
    return await get_one_carpeta(id)
