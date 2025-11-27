from fastapi import APIRouter, status

from models.usuario import User
from controllers.usuario import (
    create_user,
    update_user,
    delete_user,
    get_all_users,
    get_one_user
)

router = APIRouter(prefix="/usuarios")

@router.get("/", tags=["Usuarios"], status_code=status.HTTP_200_OK)
async def get_all_usuarios():
    result = await get_all_users()
    return result

@router.post("/", tags=["Usuarios"], status_code=status.HTTP_201_CREATED)
async def create_new_usuario(usuario_data: User):
    result = await create_user(usuario_data)
    return result

@router.put("/{id}", tags=["Usuarios"], status_code=status.HTTP_200_OK)
async def update_usuario_info(usuario_data: User, id: int):
    usuario_data.id = id
    result = await update_user(usuario_data)
    return result

@router.delete("/{id}", tags=["Usuarios"], status_code=status.HTTP_200_OK)
async def delete_usuario(id: int):
    status_message = await delete_user(id)
    return {"detail": status_message}

@router.get("/{id}", tags=["Usuarios"], status_code=status.HTTP_200_OK)
async def get_one_usuario(id: int):
    result = await get_one_user(id)
    return result
