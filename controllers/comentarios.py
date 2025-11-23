import json
from fastapi import HTTPException
from models.comentarios import Comentario
from utils.database import execute_query_json

async def get_file_comments(id_archivo: int) -> list:
    """Obtener todos los comentarios de un archivo"""
    sql = """
        SELECT 
            C.ID,
            C.ID_USUARIO,
            U.NOMBRE AS NOMBRE_USUARIO,
            C.ID_ARCHIVO,
            C.TEXTO,
            C.FECHA
        FROM GD.COMENTARIOS C
        LEFT JOIN GD.USUARIO U ON C.ID_USUARIO = U.ID
        WHERE C.ID_ARCHIVO = ?
        ORDER BY C.FECHA DESC
    """
    
    try:
        result = await execute_query_json(sql, [id_archivo])
        if not result:
            raise HTTPException(status_code=404, detail="No hay comentarios para este archivo")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def get_comment_one(id: int) -> dict:
    """Obtener un comentario específico"""
    sql = """
        SELECT 
            C.ID,
            C.ID_USUARIO,
            U.NOMBRE AS NOMBRE_USUARIO,
            C.ID_ARCHIVO,
            C.TEXTO,
            C.FECHA
        FROM GD.COMENTARIOS C
        LEFT JOIN GD.USUARIO U ON C.ID_USUARIO = U.ID
        WHERE C.ID = ?
    """
    
    try:
        result = await execute_query_json(sql, [id])
        if len(result) == 0:
            raise HTTPException(status_code=404, detail="Comentario no encontrado")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def create_comment(comentario) -> dict:
    """Crear un nuevo comentario"""
    sql = """
        INSERT INTO GD.COMENTARIOS (ID_USUARIO, ID_ARCHIVO, TEXTO, FECHA)
        VALUES (?, ?, ?, SYSDATE)
    """
    
    params = [
        comentario.id_usuario,
        comentario.id_archivo,
        comentario.texto
    ]
    
    try:
        await execute_query_json(sql, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    sql_find = """
        SELECT ID, ID_USUARIO, ID_ARCHIVO, TEXTO, FECHA
        FROM GD.COMENTARIOS
        WHERE TEXTO = ? AND ID_USUARIO = ?
        ORDER BY FECHA DESC
    """
    
    try:
        result = await execute_query_json(sql_find, [comentario.texto, comentario.id_usuario])
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def update_comment(comentario) -> dict:
    """Actualizar un comentario"""
    data = comentario.model_dump(exclude_none=True)
    
    keys = list(data.keys())
    if "id" in keys:
        keys.remove("id")
    
    if not keys:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")
    
    set_vars = ", ".join([f"{k} = ?" for k in keys])
    
    sql = f"""
        UPDATE GD.COMENTARIOS
        SET {set_vars}
        WHERE ID = ?
    """
    
    params = [data[k] for k in keys] + [comentario.id]
    
    try:
        await execute_query_json(sql, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    sql_find = """
        SELECT ID, ID_USUARIO, ID_ARCHIVO, TEXTO, FECHA
        FROM GD.COMENTARIOS
        WHERE ID = ?
    """
    
    try:
        result = await execute_query_json(sql_find, [comentario.id])
        return result[0] if len(result) else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def delete_comment(id: int) -> str:
    """Eliminar un comentario"""
    sql = "DELETE FROM GD.COMENTARIOS WHERE ID = ?"
    
    try:
        await execute_query_json(sql, [id], needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
