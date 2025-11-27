from fastapi import APIRouter, status
from models.compartidos import Compartido, CompartidoUpdate
from controllers.compartidos import get_all_compartidos, get_one_compartido, create_compartido, update_compartido, delete_compartido

router = APIRouter(prefix="/compartidos")

@router.get("/", tags=["Compartidos"], status_code=status.HTTP_200_OK)
async def route_get_all_compartidos():
    return await get_all_compartidos()

@router.get("/{id}", tags=["Compartidos"], status_code=status.HTTP_200_OK)
async def route_get_one_compartido(id: int):
    return await get_one_compartido(id)

@router.post("/", tags=["Compartidos"], status_code=status.HTTP_201_CREATED)
async def route_create_compartido(compartido_data: Compartido):
    return await create_compartido(compartido_data)

@router.put("/{id}", tags=["Compartidos"], status_code=status.HTTP_200_OK)
async def route_update_compartido(id: int, compartido_data: CompartidoUpdate):
    return await update_compartido(id, compartido_data)

@router.delete("/{id}", tags=["Compartidos"], status_code=status.HTTP_200_OK)
async def route_delete_compartido(id: int):
    return {"message": await delete_compartido(id)}
