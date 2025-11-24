from fastapi import APIRouter, status
from models.favoritos import Favorito, FavoritoUpdate
from controllers.favoritos import (
    get_one_favorito,
    get_favoritos_by_usuario,
    create_favorito,
    delete_favorito,
    update_favorito
)

router = APIRouter(prefix="/favoritos")

@router.get("/", tags=["Favoritos"], status_code=status.HTTP_200_OK)
async def get_all_favoritos_route(id_usuario: int):
    return await get_favoritos_by_usuario(id_usuario)

@router.post("/", tags=["Favoritos"], status_code=status.HTTP_201_CREATED)
async def create_new_favorito(favorito_data: Favorito):
    return await create_favorito(favorito_data)

@router.put("/{id}", tags=["Favoritos"], status_code=status.HTTP_200_OK)
async def update_favorito_route(id: int, body: FavoritoUpdate):
    return await update_favorito(id, body)


@router.delete("/{id}", tags=["Favoritos"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_favorito_route(id: int):
    return await delete_favorito(id)

@router.get("/{id}", tags=["Favoritos"], status_code=status.HTTP_200_OK)
async def get_one_favorito_route(id: int):
    return await get_one_favorito(id)