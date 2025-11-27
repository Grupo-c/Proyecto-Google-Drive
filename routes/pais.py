from fastapi import APIRouter, status
from models.pais import Pais
from controllers.pais import (
    get_all_paises,
    get_one_pais,
    create_pais,
    update_pais,
    delete_pais
)

router = APIRouter(prefix="/paises")

@router.get("/", tags=["Paises"])
async def all_paises():
    return await get_all_paises()

@router.get("/{id}", tags=["Paises"])
async def one_pais(id: int):
    return await get_one_pais(id)

@router.post("/", tags=["Paises"], status_code=status.HTTP_201_CREATED)
async def new_pais(data: Pais):
    return await create_pais(data)

@router.put("/{id}", tags=["Paises"])
async def update_p(id: int, data: Pais):
    return await update_pais(id, data)

@router.delete("/{id}", tags=["Paises"])
async def delete_p(id: int):
    return await delete_pais(id)
