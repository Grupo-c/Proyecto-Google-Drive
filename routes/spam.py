from fastapi import APIRouter, status

from models.spam import Spam
from controllers.spam import (
    get_one_spam,
    get_spam_by_usuario,
    create_spam,
    delete_spam,
)

router = APIRouter(prefix="/spam")

@router.get("/usuario/{id_usuario}", tags=["Spam"], status_code=status.HTTP_200_OK)
async def get_spam_usuario(id_usuario: int):
    return await get_spam_by_usuario(id_usuario)

@router.get("/{id}", tags=["Spam"], status_code=status.HTTP_200_OK)
async def get_spam(id: int):
    return await get_one_spam(id)

@router.post("/", tags=["Spam"], status_code=status.HTTP_201_CREATED)
async def add_spam(spam: Spam):
    result = await create_spam(spam)
    return result

@router.delete("/{id}", tags=["Spam"], status_code=status.HTTP_204_NO_CONTENT)
async def remove_spam(id: int):
    await delete_spam(id)
    return {"message": f"Spam {id} eliminado"}