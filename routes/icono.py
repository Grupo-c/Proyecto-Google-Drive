from fastapi import APIRouter, status
from models.icono import Icono, IconoUpdate
from controllers.icono import (
    get_all_iconos as controller_get_all_iconos,
    get_one_icono as controller_get_one_icono,
    create_icono as controller_create_icono,
    update_icono as controller_update_icono,
    delete_icono as controller_delete_icono
)

router = APIRouter(prefix="/iconos")

@router.get("/", tags=["Iconos"], status_code=status.HTTP_200_OK)
async def route_get_all_iconos():
    return await controller_get_all_iconos()

@router.get("/{id}", tags=["Iconos"], status_code=status.HTTP_200_OK)
async def route_get_one_icono(id: int):
    return await controller_get_one_icono(id)

@router.post("/", tags=["Iconos"], status_code=status.HTTP_201_CREATED)
async def route_create_icono(icono_data: Icono):
    return await controller_create_icono(icono_data)

@router.put("/{id}", tags=["Iconos"], status_code=status.HTTP_200_OK)
async def route_update_icono(id: int, icono_data: IconoUpdate):
    return await controller_update_icono(id, icono_data)

@router.delete("/{id}", tags=["Iconos"], status_code=status.HTTP_200_OK)
async def route_delete_icono(id: int):
    return await controller_delete_icono(id)
