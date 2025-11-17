from fastapi import HTTPException
from models.favoritos import Favorito
from utils.database import execute_query_json

async def get_one_favorito(id_favorito: int) -> Favorito:
    sql = "SELECT * FROM GD.FAVORITOS WHERE id_favorito = ?"
    try:
        result = await execute_query_json(sql, [id_favorito])
        if len(result) == 0:
            raise HTTPException(status_code=404, detail="Favorito no encontrado")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
async def get_favoritos_by_usuario(id_usuario: int) -> list[Favorito]:
    sql = "SELECT * FROM GD.FAVORITOS WHERE id_usuario = ?"
    try:
        result = await execute_query_json(sql, [id_usuario])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
async def create_favorito(favorito: Favorito) -> Favorito:
    sql = """
        INSERT INTO GD.FAVORITOS (id_usuario, id_carpeta, id_archivo, fecha_agregado)
        VALUES (?, ?, ?, ?)
    """
    params = [
        favorito.id_usuario,
        favorito.id_carpeta,
        favorito.id_archivo,
        favorito.fecha_agregado
    ]
    try:
        await execute_query_json(sql, params, needs_commit=True)
        sql_find = "SELECT TOP 1 * FROM GD.FAVORITOS WHERE id_usuario = ? AND id_recurso = ? ORDER BY id_favorito DESC"
        result = await execute_query_json(sql_find, [favorito.id_usuario, favorito.id_recurso])
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def delete_favorito(id_favorito: int) -> None:
    sql = "DELETE FROM GD.FAVORITOS WHERE id_favorito = ?"
    try:
        await execute_query_json(sql, [id_favorito], needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
async def update_favorito(favorito: Favorito) -> Favorito:
    data = favorito.model_dump(exclude_none=True)
    keys = list(data.keys())
    keys.remove("id_favorito")
    set_vars = " = ?, ".join(keys) + " = ?"
    sql = f"UPDATE GD.FAVORITOS SET {set_vars} WHERE id_favorito = ?"
    params = [data[k] for k in keys] + [favorito.id_favorito]
    try:
        await execute_query_json(sql, params, needs_commit=True)
        sql_find = "SELECT * FROM GD.FAVORITOS WHERE id_favorito = ?"
        result = await execute_query_json(sql_find, [favorito.id_favorito])
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")