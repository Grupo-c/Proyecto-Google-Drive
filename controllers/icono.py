import json
from fastapi import HTTPException
from models.icono import Icono
from utils.database import execute_query_json

# Obtener todos los iconos
async def get_all_icons() -> list:
    sql = """
        SELECT ID, NOMBRE, URL
        FROM GD.ICONOS
    """
    try:
        result = await execute_query_json(sql)
        if not result:
            raise HTTPException(status_code=404, detail="No hay iconos disponibles")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Obtener un icono por ID
async def get_one_icon(id: int) -> dict:
    sql = """
        SELECT ID, NOMBRE, URL
        FROM GD.ICONOS
        WHERE ID = :id
    """
    try:
        result = await execute_query_json(sql, {"id": id})
        if not result:
            raise HTTPException(status_code=404, detail="Icono no encontrado")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Crear un icono
async def create_icon(icono: Icono) -> dict:
    sql = """
        INSERT INTO GD.ICONOS (NOMBRE, URL)
        VALUES (:nombre, :url)
    """
    params = {
        "nombre": icono.nombre,
        "url": icono.url
    }
    try:
        await execute_query_json(sql, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    sql_find = """
        SELECT ID, NOMBRE, URL
        FROM GD.ICONOS
        WHERE NOMBRE = :nombre
        ORDER BY ID DESC
    """
    try:
        result = await execute_query_json(sql_find, {"nombre": icono.nombre})
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Actualizar un icono
async def update_icon(icono: Icono) -> dict:
    data = icono.model_dump(exclude_none=True)
    keys = [k for k in data if k != "id"]

    if not keys:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")

    set_clause = ", ".join([f"{k} = :{k}" for k in keys])
    sql = f"UPDATE GD.ICONOS SET {set_clause} WHERE ID = :id"

    params = {k: data[k] for k in keys}
    params["id"] = icono.id

    try:
        await execute_query_json(sql, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    sql_find = """
        SELECT ID, NOMBRE, URL
        FROM GD.ICONOS
        WHERE ID = :id
    """
    try:
        result = await execute_query_json(sql_find, {"id": icono.id})
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Eliminar un icono
async def delete_icon(id: int) -> str:
    sql = "DELETE FROM GD.ICONOS WHERE ID = :id"
    try:
        await execute_query_json(sql, {"id": id}, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
