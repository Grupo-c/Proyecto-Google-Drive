from fastapi import APIRouter, status
from models.comentarios import Comentario
from controllers.comentarios import get_all_comments, get_one_comment, create_comment, update_comment, delete_comment

router = APIRouter(prefix="/comentarios")

@router.get("/", tags=["Comentarios"], status_code=status.HTTP_200_OK)
async def get_all_comentarios():
    return await get_all_comments()

@router.get("/{id}", tags=["Comentarios"], status_code=status.HTTP_200_OK)
async def get_one_comentario(id: int):
    return await get_one_comment(id)

@router.post("/", tags=["Comentarios"], status_code=status.HTTP_201_CREATED)
async def create_new_comentario(comentario_data: Comentario):
    return await create_comment(comentario_data)

@router.put("/{id}", tags=["Comentarios"], status_code=status.HTTP_200_OK)
async def update_comentario_info(comentario_data: Comentario, id: int):
    comentario_data.id = id
    return await update_comment(comentario_data)

@router.delete("/{id}", tags=["Comentarios"], status_code=status.HTTP_200_OK)
async def delete_comentario(id: int):
    return {"message": await delete_comment(id)}
