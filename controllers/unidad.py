import json
from fastapi import HTTPException
from models.unidad import Unidad, UnidadUpdate
from utils.database import execute_query_json

async def get_one_unidad(id: int) -> Unidad:
    sql = """
        SELECT 
            u.ID, 
            u.ID_USUARIO,
            CASE 
                WHEN u.CAPACIDAD_TOTAL >= 1024 
                    THEN ROUND(u.CAPACIDAD_TOTAL / 1024, 2) || ' GB'
                ELSE u.CAPACIDAD_TOTAL || ' MB'
            END AS CAPACIDAD_TOTAL,
            CASE 
                WHEN u.CAPACIDAD_ACTUAL >= 1024 
                    THEN ROUND(u.CAPACIDAD_ACTUAL / 1024, 2) || ' GB'
                ELSE u.CAPACIDAD_ACTUAL || ' MB'
            END AS CAPACIDAD_ACTUAL,
            u.ID_MEMBRESIA,
            u.FECHA_COMPRA,
            u.FECHA_EXPIRACION,
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
        SELECT 
            u.ID, 
            u.ID_USUARIO,
            CASE 
                WHEN u.CAPACIDAD_TOTAL >= 1024 
                    THEN ROUND(u.CAPACIDAD_TOTAL / 1024, 2) || ' GB'
                ELSE u.CAPACIDAD_TOTAL || ' MB'
            END AS CAPACIDAD_TOTAL,
            CASE 
                WHEN u.CAPACIDAD_ACTUAL >= 1024 
                    THEN ROUND(u.CAPACIDAD_ACTUAL / 1024, 2) || ' GB'
                ELSE u.CAPACIDAD_ACTUAL || ' MB'
            END AS CAPACIDAD_ACTUAL,
            u.ID_MEMBRESIA,
            u.FECHA_COMPRA,
            u.FECHA_EXPIRACION,
            us.NOMBRE AS NOMBRE_USUARIO
        FROM UNIDAD u
        LEFT JOIN USUARIO us ON u.ID_USUARIO = us.ID
    """
    try:
        return await execute_query_json(sql)

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
            CASE 
                WHEN u.CAPACIDAD_ACTUAL >= 1024 
                    THEN ROUND(u.CAPACIDAD_ACTUAL / 1024, 2) || ' GB'
                ELSE u.CAPACIDAD_ACTUAL || ' MB'
            END AS CAPACIDAD_ACTUAL,
            CASE 
                WHEN u.CAPACIDAD_TOTAL >= 1024 
                    THEN ROUND(u.CAPACIDAD_TOTAL / 1024, 2) || ' GB'
                ELSE u.CAPACIDAD_TOTAL || ' MB'
            END AS CAPACIDAD_TOTAL,
            LEFT JOIN USUARIO us ON u.ID_USUARIO = us.ID
            WHERE u.ID_USUARIO = :id_usuario
            ORDER BY u.ID DESC
        """
        result = await execute_query_json(sql_find, {"id_usuario": unidad.id_usuario})
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def update_unidad(data: UnidadUpdate) -> Unidad:
    sql_check = "SELECT ID FROM UNIDAD WHERE ID = :id"
    exists = await execute_query_json(sql_check, {"id": data.id})

    if not exists:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")

    sql_update = """
        UPDATE UNIDAD
        SET ID_MEMBRESIA = :id_membresia
        WHERE ID = :id
    """

    await execute_query_json(sql_update, {
        "id": data.id,
        "id_membresia": data.id_membresia
    }, needs_commit=True)

    sql_get = """
        SELECT 
            u.ID, 
            u.ID_USUARIO,
            CASE 
                WHEN u.CAPACIDAD_TOTAL >= 1024 
                    THEN ROUND(u.CAPACIDAD_TOTAL / 1024, 2) || ' GB'
                ELSE u.CAPACIDAD_TOTAL || ' MB'
            END AS CAPACIDAD_TOTAL,
            CASE 
                WHEN u.CAPACIDAD_ACTUAL >= 1024 
                    THEN ROUND(u.CAPACIDAD_ACTUAL / 1024, 2) || ' GB'
                ELSE u.CAPACIDAD_ACTUAL || ' MB'
            END AS CAPACIDAD_ACTUAL,
            u.ID_MEMBRESIA,
            u.FECHA_COMPRA,
            u.FECHA_EXPIRACION,
            us.NOMBRE AS NOMBRE_USUARIO
        FROM UNIDAD u
        LEFT JOIN USUARIO us ON u.ID_USUARIO = us.ID
        WHERE u.ID = :id
    """

    result = await execute_query_json(sql_get, {"id": data.id})
    return result[0]

async def delete_unidad(id: int) -> str:
    sql = "DELETE FROM UNIDAD WHERE ID = :id"
    try:
        await execute_query_json(sql, {"id": id}, needs_commit=True)
        return "DELETED"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
