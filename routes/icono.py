from fastapi import APIRouter, status
from models.icono import Icono
from controllers.icono import (
    get_all_icons,
    get_one_icon,
    create_icon,
    update_icon,
    delete_icon
)

router = APIRouter(prefix="/Icono")

# Obtener todos los iconos
@router.get("/", tags=["Icono"], status_code=status.HTTP_200_OK)
async def get_all_icons_route():
    result = await get_all_icons()
    return result

# Obtener un icono por ID
@router.get("/{id}", tags=["Icono"], status_code=status.HTTP_200_OK)
async def get_icon_by_id(id: int):
    result = await get_one_icon(id)
    return result

# Crear un nuevo icono
@router.post("/", tags=["Icono"], status_code=status.HTTP_201_CREATED)
async def create_new_icon(icono_data: Icono):
    result = await create_icon(icono_data)
    return result

# Actualizar un icono por ID
@router.put("/{id}", tags=["Icono"], status_code=status.HTTP_200_OK)
async def update_icon_by_id(icono_data: Icono, id: int):
    icono_data.id = id
    result = await update_icon(icono_data)
    return result

# Eliminar un icono por ID
@router.delete("/{id}", tags=["Icono"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_icon_by_id(id: int):
    await delete_icon(id)
    return None
