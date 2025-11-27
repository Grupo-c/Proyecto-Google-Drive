from fastapi import APIRouter, status
from models.icono import Icono, IconoUpdate
from controllers.icono import (
    get_all_iconos,
    get_one_icono,
    create_icono,
    update_icono,
    delete_icono
)

router = APIRouter(prefix="/iconos")

@router.get("/", tags=["Iconos"], status_code=status.HTTP_200_OK)
async def get_all_iconos():
    return await get_all_iconos()

@router.get("/{id}", tags=["Iconos"], status_code=status.HTTP_200_OK)
async def get_one_icono(id: int):
    return await get_one_icono(id)

@router.post("/", tags=["Iconos"], status_code=status.HTTP_201_CREATED)
async def create_new_icono(icono_data: Icono):
    return await create_icono(icono_data)

@router.put("/{id}", tags=["Iconos"], status_code=status.HTTP_200_OK)
async def update_icono_info(id: int, icono_data: IconoUpdate):
    return await update_icono(id, icono_data)

@router.delete("/{id}", tags=["Iconos"], status_code=status.HTTP_200_OK)
async def delete_icono(id: int):
    return {"message": await delete_icono(id)}
