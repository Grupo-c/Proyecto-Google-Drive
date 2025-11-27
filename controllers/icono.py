from fastapi import HTTPException
from models.icono import Icono, IconoUpdate
from utils.database import execute_query_json

async def get_one_icono(id: int) -> Icono:
    sql = "SELECT * FROM ICONOS WHERE ID = :id"
    try:
        result = await execute_query_json(sql, {"id": id})
        if not result:
            raise HTTPException(status_code=404, detail="Icono no encontrado")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_all_iconos() -> list[Icono]:
    sql = "SELECT * FROM ICONOS"
    try:
        return await execute_query_json(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def create_icono(icono: Icono) -> Icono:
    sql = "INSERT INTO ICONOS (NOMBRE, URL) VALUES (:nombre, :url)"
    params = {"nombre": icono.nombre, "url": icono.url}
    try:
        await execute_query_json(sql, params, needs_commit=True)
        result = await execute_query_json(
            "SELECT * FROM ICONOS WHERE NOMBRE = :nombre AND URL = :url ORDER BY ID DESC",
            params
        )
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_icono(id: int, icono_update: IconoUpdate) -> Icono:
    data = icono_update.model_dump(exclude_none=True)
    if not data:
        raise HTTPException(status_code=400, detail="No se proporcionaron campos para actualizar")

    set_clause = ", ".join([f"{k} = :{k}" for k in data.keys()])
    sql = f"UPDATE ICONOS SET {set_clause} WHERE ID = :id"
    params = {**data, "id": id}
    try:
        await execute_query_json(sql, params, needs_commit=True)
        result = await execute_query_json("SELECT * FROM ICONOS WHERE ID = :id", {"id": id})
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def delete_icono(id: int) -> str:
    sql = "DELETE FROM ICONOS WHERE ID = :id"
    try:
        await execute_query_json(sql, {"id": id}, needs_commit=True)
        return f"Icono con id {id} eliminado correctamente."
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))