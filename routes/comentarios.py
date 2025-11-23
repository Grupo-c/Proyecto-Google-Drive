from fastapi import APIRouter, status
from models.comentarios import Comentario
from controllers.comentarios import (
    get_comments_by_file,
    get_one_comment,
    create_comment,
    update_comment,
    delete_comment
)

router = APIRouter(prefix="/comments")

# Obtener todos los comentarios de un archivo
@router.get("/", tags=["Comments"], status_code=status.HTTP_200_OK)
async def get_all_comments_by_file(id_archivo: int):
    result = await get_comments_by_file(id_archivo)
    return result

# Crear un nuevo comentario
@router.post("/", tags=["Comments"], status_code=status.HTTP_201_CREATED)
async def create_new_comment(comentario_data: Comentario):
    result = await create_comment(comentario_data)
    return result

# Obtener un comentario por ID
@router.get("/{id}", tags=["Comments"], status_code=status.HTTP_200_OK)
async def get_comment_by_id(id: int):
    result = await get_one_comment(id)
    return result

# Actualizar un comentario por ID
@router.put("/{id}", tags=["Comments"], status_code=status.HTTP_200_OK)
async def update_comment_by_id(comentario_data: Comentario, id: int):
    comentario_data.id = id
    result = await update_comment(comentario_data)
    return result

# Eliminar un comentario por ID
@router.delete("/{id}", tags=["Comments"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment_by_id(id: int):
    await delete_comment(id)
    return None
