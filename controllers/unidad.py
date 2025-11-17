import json
from fastapi import HTTPException
from models.unidad import Unidad
from utils.database import execute_query_json

async def get_one_unidad(id: int) -> Unidad:
    sql = "SELECT * FROM GD.UNIDAD WHERE id = ?"
    try:
        result = await execute_query_json(sql, [id])
        if len(result) == 0:
            raise HTTPException(status_code=404, detail="Unidad no encontrada")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def get_all_unidades() -> list[Unidad]:
    sql = "SELECT * FROM GD.UNIDAD"
    try:
        result = await execute_query_json(sql)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def create_unidad(unidad: Unidad) -> Unidad:
    sql = """
        INSERT INTO GD.UNIDAD (id_usuario, capacidad_total, capacidad_actual, id_membresia, fecha_compra, fecha_expiracion)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    params = [
        unidad.id_usuario,
        unidad.capacidad_total,
        unidad.capacidad_actual,
        unidad.id_membresia,
        unidad.fecha_compra,
        unidad.fecha_expiracion
    ]
    try:
        await execute_query_json(sql, params, needs_commit=True)
        sql_find = "SELECT TOP 1 * FROM GD.UNIDAD WHERE id_usuario = ? ORDER BY id DESC"
        result = await execute_query_json(sql_find, [unidad.id_usuario])
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def update_unidad(unidad: Unidad) -> Unidad:
    data = unidad.model_dump(exclude_none=True)
    keys = list(data.keys())
    keys.remove("id")
    set_vars = " = ?, ".join(keys) + " = ?"
    sql = f"UPDATE GD.UNIDAD SET {set_vars} WHERE id = ?"
    params = [data[k] for k in keys] + [unidad.id]
    try:
        await execute_query_json(sql, params, needs_commit=True)
        sql_find = "SELECT * FROM GD.UNIDAD WHERE id = ?"
        result = await execute_query_json(sql_find, [unidad.id])
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

async def delete_unidad(id: int) -> str:
    sql = "DELETE FROM GD.UNIDAD WHERE id = ?"
    try:
        await execute_query_json(sql, [id], needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
