import json
from fastapi import HTTPException
from models.unidad import Unidad
from utils.database import execute_query_json

async def get_one_unidad(id: int) -> Unidad:
    sql = """
        SELECT u.ID, u.ID_MEMBRESIA,
            us.NOMBRE AS NOMBRE_USUARIO
        FROM UNIDAD u
        LEFT JOIN USUARIO us ON u.ID_USUARIO = us.ID
        WHERE u.ID = :id
    """
    try:
        result = await execute_query_json(sql, {"id": id})
        if not result:
            raise HTTPException(status_code=404, detail="Unidad no encontrada")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_all_unidades() -> list[Unidad]:
    sql = """
        SELECT u.ID, u.ID_MEMBRESIA,
            us.NOMBRE AS NOMBRE_USUARIO
        FROM UNIDAD u
        LEFT JOIN USUARIO us ON u.ID_USUARIO = us.ID
    """
    try:
        result = await execute_query_json(sql)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def create_unidad(unidad: Unidad) -> Unidad:
    sql = """
        INSERT INTO UNIDAD (ID_USUARIO, ID_MEMBRESIA)
        VALUES (:id_usuario, :id_membresia)
    """
    params = {
        "id_usuario": unidad.id_usuario,
        "id_membresia": unidad.id_membresia
    }
    try:
        await execute_query_json(sql, params, needs_commit=True)
        sql_find = """
            SELECT u.ID, u.ID_MEMBRESIA,
                us.NOMBRE AS NOMBRE_USUARIO
            FROM UNIDAD u
            LEFT JOIN USUARIO us ON u.ID_USUARIO = us.ID
            WHERE u.ID_USUARIO = :id_usuario
            ORDER BY u.ID DESC
        """
        result = await execute_query_json(sql_find, {"id_usuario": unidad.id_usuario})
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def update_unidad(unidad: Unidad) -> Unidad:
    raise HTTPException(status_code=400, detail="No hay campos editables para Unidad")

async def delete_unidad(id: int) -> str:
    sql = "DELETE FROM UNIDAD WHERE ID = :id"
    try:
        await execute_query_json(sql, {"id": id}, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
