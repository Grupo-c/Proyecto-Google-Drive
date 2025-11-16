import json
from fastapi import HTTPException
from models.carpeta import Carpeta
from utils.database import execute_query_json

async def get_one_carpeta(id: int) -> Carpeta:
    sql = "SELECT * FROM GD.CARPETA WHERE id = ?"
    try:
        result = await execute_query_json(sql, [id])
        if len(result) == 0:
            raise HTTPException(status_code=404, detail="Carpeta no encontrada")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_all_carpetas() -> list[Carpeta]:
    sql = "SELECT * FROM GD.CARPETA"
    try:
        result = await execute_query_json(sql)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def create_carpeta(carpeta: Carpeta) -> Carpeta:
    sql = """
        INSERT INTO GD.CARPETA (id_usuario, id_carpeta_padre, nombre, tamaño, fecha_creacion, fecha_modificacion, visibilidad)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    params = [
        carpeta.id_usuario,
        carpeta.id_carpeta_padre,
        carpeta.nombre,
        carpeta.tamaño,
        carpeta.fecha_creacion,
        carpeta.fecha_modificacion,
        carpeta.visibilidad
    ]
    try:
        await execute_query_json(sql, params, needs_commit=True)
        # Traer la carpeta recién creada
        sql_find = "SELECT * FROM GD.CARPETA WHERE nombre = ? AND id_usuario = ?"
        result = await execute_query_json(sql_find, [carpeta.nombre, carpeta.id_usuario])
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def update_carpeta(carpeta: Carpeta) -> Carpeta:
    data = carpeta.model_dump(exclude_none=True)
    keys = list(data.keys())
    keys.remove("id")
    set_vars = " = ?, ".join(keys) + " = ?"
    sql = f"UPDATE GD.CARPETA SET {set_vars} WHERE id = ?"
    params = [data[k] for k in keys] + [carpeta.id]
    try:
        await execute_query_json(sql, params, needs_commit=True)
        sql_find = "SELECT * FROM GD.CARPETA WHERE id = ?"
        result = await execute_query_json(sql_find, [carpeta.id])
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def delete_carpeta(id: int) -> str:
    sql = "DELETE FROM GD.CARPETA WHERE id = ?"
    try:
        await execute_query_json(sql, [id], needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
