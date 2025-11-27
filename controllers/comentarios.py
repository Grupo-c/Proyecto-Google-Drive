from fastapi import HTTPException
from models.comentarios import Comentario
from utils.database import execute_query_json

async def get_one_comment(id: int) -> Comentario:
    sql = "SELECT * FROM COMENTARIOS WHERE ID = :id"
    try:
        result = await execute_query_json(sql, {"id": id})
        if not result:
            raise HTTPException(status_code=404, detail="Comentario no encontrado")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_all_comments() -> list[Comentario]:
    sql = "SELECT * FROM COMENTARIOS"
    try:
        return await execute_query_json(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def create_comment(comment: Comentario) -> Comentario:
    sql = """INSERT INTO COMENTARIOS (ID_USUARIO_COMENTADOR, ID_ARCHIVO, TEXTO) 
             VALUES (:id_usuario_comentador, :id_archivo, :texto)"""
    params = {
        "id_usuario_comentador": comment.id_usuario_comentador,
        "id_archivo": comment.id_archivo,
        "texto": comment.texto
    }
    try:
        await execute_query_json(sql, params, needs_commit=True)
        result = await execute_query_json(
            "SELECT * FROM COMENTARIOS WHERE ID_USUARIO_COMENTADOR=:id_usuario_comentador AND ID_ARCHIVO=:id_archivo ORDER BY ID DESC",
            params
        )
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_comment(comment: Comentario) -> Comentario:
    data = comment.model_dump(exclude_none=True)
    keys = [k for k in data if k != "id"]
    set_clause = ", ".join([f"{k} = :{k}" for k in keys])
    sql = f"UPDATE COMENTARIOS SET {set_clause} WHERE ID = :id"
    params = {**{k: data[k] for k in keys}, "id": comment.id}
    try:
        await execute_query_json(sql, params, needs_commit=True)
        result = await execute_query_json("SELECT * FROM COMENTARIOS WHERE ID = :id", {"id": comment.id})
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def delete_comment(id: int) -> str:
    sql = "DELETE FROM COMENTARIOS WHERE ID = :id"
    try:
        await execute_query_json(sql, {"id": id}, needs_commit=True)
        return f"Comentario con id {id} eliminado correctamente."
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
