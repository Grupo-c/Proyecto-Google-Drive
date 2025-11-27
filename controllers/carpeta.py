import json
from fastapi import HTTPException
from models.carpeta import Carpeta
from utils.database import execute_query_json

async def get_one_carpeta(id: int) -> Carpeta:
    sql = """
        SELECT c.ID, c.NOMBRE,
            u.NOMBRE AS NOMBRE_USUARIO,
            cp.NOMBRE AS NOMBRE_CARPETA_PADRE
        FROM CARPETA c
        LEFT JOIN USUARIO u ON c.ID_USUARIO = u.ID
        LEFT JOIN CARPETA cp ON c.ID_CARPETA_PADRE = cp.ID
        WHERE c.ID = :id
    """
    try:
        result = await execute_query_json(sql, {"id": id})
        if not result:
            raise HTTPException(status_code=404, detail="Carpeta no encontrada")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_all_carpetas() -> list[Carpeta]:
    sql = """
        SELECT c.ID, c.NOMBRE,
            u.NOMBRE AS NOMBRE_USUARIO,
            cp.NOMBRE AS NOMBRE_CARPETA_PADRE
        FROM CARPETA c
        LEFT JOIN USUARIO u ON c.ID_USUARIO = u.ID
        LEFT JOIN CARPETA cp ON c.ID_CARPETA_PADRE = cp.ID
    """
    try:
        result = await execute_query_json(sql)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def create_carpeta(carpeta: Carpeta) -> Carpeta:
    sql = """
        INSERT INTO CARPETA (ID_USUARIO, ID_CARPETA_PADRE, NOMBRE)
        VALUES (:id_usuario, :id_carpeta_padre, :nombre)
    """
    params = {
        "id_usuario": carpeta.id_usuario,
        "id_carpeta_padre": carpeta.id_carpeta_padre,
        "nombre": carpeta.nombre
    }
    try:
        await execute_query_json(sql, params, needs_commit=True)
        sql_find = """
            SELECT c.ID, c.NOMBRE,
                u.NOMBRE AS NOMBRE_USUARIO,
                cp.NOMBRE AS NOMBRE_CARPETA_PADRE
            FROM CARPETA c
            LEFT JOIN USUARIO u ON c.ID_USUARIO = u.ID
            LEFT JOIN CARPETA cp ON c.ID_CARPETA_PADRE = cp.ID
            WHERE c.NOMBRE = :nombre AND c.ID_USUARIO = :id_usuario
            ORDER BY c.ID DESC
        """
        result = await execute_query_json(sql_find, params)
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def update_carpeta(carpeta: Carpeta) -> Carpeta:
    data = carpeta.model_dump(exclude_none=True)
    keys = []
    if "nombre" in data:
        keys.append("NOMBRE")
    if "id_carpeta_padre" in data:
        keys.append("ID_CARPETA_PADRE")
    if not keys:
        raise HTTPException(status_code=400, detail="No hay campos válidos para actualizar")
    
    set_vars = ", ".join([f"{k} = :{k.lower()}" for k in keys])
    sql = f"UPDATE CARPETA SET {set_vars} WHERE ID = :id"
    params = {k.lower(): data[k.lower()] for k in keys}
    params["id"] = carpeta.id

    try:
        await execute_query_json(sql, params, needs_commit=True)
        sql_find = """
            SELECT c.ID, c.NOMBRE,
                u.NOMBRE AS NOMBRE_USUARIO,
                cp.NOMBRE AS NOMBRE_CARPETA_PADRE
            FROM CARPETA c
            LEFT JOIN USUARIO u ON c.ID_USUARIO = u.ID
            LEFT JOIN CARPETA cp ON c.ID_CARPETA_PADRE = cp.ID
            WHERE c.ID = :id
        """
        result = await execute_query_json(sql_find, {"id": carpeta.id})
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def delete_carpeta(id: int) -> str:
    sql = "DELETE FROM CARPETA WHERE ID = :id"
    try:
        await execute_query_json(sql, {"id": id}, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
