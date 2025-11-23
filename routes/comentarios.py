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

@router.get("/", tags=["Comments"], status_code=status.HTTP_200_OK)
async def get_all_comments_by_file(id_archivo: int):
    """Get all comments from a file"""
    result = await get_comments_by_file(id_archivo)
    return result

@router.post("/", tags=["Comments"], status_code=status.HTTP_201_CREATED)
async def create_new_comment(comentario_data: Comentario):
    """Create a new comment"""
    result = await create_comment(comentario_data)
    return result

@router.get("/{id}", tags=["Comments"], status_code=status.HTTP_200_OK)
async def get_comment_by_id(id: int):
    """Get a specific comment by ID"""
    result = await get_one_comment(id)
    return result

@router.put("/{id}", tags=["Comments"], status_code=status.HTTP_200_OK)
async def update_comment_by_id(comentario_data: Comentario, id: int):
    """Update a comment"""
    comentario_data.id = id
    result = await update_comment(comentario_data)
    return result

@router.delete("/{id}", tags=["Comments"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment_by_id(id: int):
    """Delete a comment"""
    await delete_comment(id)
    return None
