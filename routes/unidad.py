from fastapi import APIRouter, status
from models.unidad import Unidad
from controllers.unidad import (
    create_unidad, update_unidad, delete_unidad,
    get_all_unidades, get_one_unidad
)

router = APIRouter(prefix="/unidades")

@router.get("/", tags=["Unidades"], status_code=status.HTTP_200_OK)
async def get_all_unidades_route():
    return await get_all_unidades()

@router.post("/", tags=["Unidades"], status_code=status.HTTP_201_CREATED)
async def create_new_unidad(unidad_data: Unidad):
    return await create_unidad(unidad_data)

@router.put("/{id}", tags=["Unidades"], status_code=status.HTTP_200_OK)
async def update_unidad_route(unidad_data: Unidad, id: int):
    unidad_data.id = id
    return await update_unidad(unidad_data)

@router.delete("/{id}", tags=["Unidades"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_unidad_route(id: int):
    return await delete_unidad(id)

@router.get("/{id}", tags=["Unidades"], status_code=status.HTTP_200_OK)
async def get_one_unidad_route(id: int):
    return await get_one_unidad(id)
