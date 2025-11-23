import json
from fastapi import HTTPException
from models.comentarios import Comentario
from utils.database import execute_query_json

# Obtener todos los comentarios de un archivo
async def get_comments_by_file(id_archivo: int) -> list:
    sql = """
        SELECT 
            C.ID,
            C.ID_USUARIO,
            U.NOMBRE AS NOMBRE_USUARIO,
            C.ID_ARCHIVO,
            C.TEXTO,
            C.FECHA
        FROM COMENTARIOS C
        LEFT JOIN USUARIO U ON C.ID_USUARIO = U.ID
        WHERE C.ID_ARCHIVO = :id_archivo
        ORDER BY C.FECHA DESC
    """
    try:
        result = await execute_query_json(sql, {"id_archivo": id_archivo})
        if not result:
            raise HTTPException(status_code=404, detail="No hay comentarios para este archivo")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Obtener un comentario por ID
async def get_one_comment(id: int) -> dict:
    sql = """
        SELECT 
            C.ID,
            C.ID_USUARIO,
            U.NOMBRE AS NOMBRE_USUARIO,
            C.ID_ARCHIVO,
            C.TEXTO,
            C.FECHA
        FROM COMENTARIOS C
        LEFT JOIN USUARIO U ON C.ID_USUARIO = U.ID
        WHERE C.ID = :id
    """
    try:
        result = await execute_query_json(sql, {"id": id})
        if not result:
            raise HTTPException(status_code=404, detail="Comentario no encontrado")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Crear un comentario
async def create_comment(comentario: Comentario) -> dict:
    sql = """
        INSERT INTO COMENTARIOS (ID_USUARIO, ID_ARCHIVO, TEXTO, FECHA)
        VALUES (:id_usuario, :id_archivo, :texto, SYSDATE)
    """
    params = {
        "id_usuario": comentario.id_usuario,
        "id_archivo": comentario.id_archivo,
        "texto": comentario.texto
    }
    try:
        await execute_query_json(sql, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    sql_find = """
        SELECT ID, ID_USUARIO, ID_ARCHIVO, TEXTO, FECHA
        FROM COMENTARIOS
        WHERE TEXTO = :texto AND ID_USUARIO = :id_usuario
        ORDER BY FECHA DESC
    """
    try:
        result = await execute_query_json(sql_find, {
            "texto": comentario.texto,
            "id_usuario": comentario.id_usuario
        })
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Actualizar un comentario
async def update_comment(comentario: Comentario) -> dict:
    data = comentario.model_dump(exclude_none=True)
    keys = [k for k in data if k != "id"]

    if not keys:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")

    set_clause = ", ".join([f"{k} = :{k}" for k in keys])
    sql = f"UPDATE COMENTARIOS SET {set_clause} WHERE ID = :id"

    params = {k: data[k] for k in keys}
    params["id"] = comentario.id

    try:
        await execute_query_json(sql, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    sql_find = "SELECT ID, ID_USUARIO, ID_ARCHIVO, TEXTO, FECHA FROM COMENTARIOS WHERE ID = :id"
    try:
        result = await execute_query_json(sql_find, {"id": comentario.id})
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Eliminar un comentario
async def delete_comment(id: int) -> str:
    sql = "DELETE FROM COMENTARIOS WHERE ID = :id"
    try:
        await execute_query_json(sql, {"id": id}, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
