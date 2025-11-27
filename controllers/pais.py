from fastapi import HTTPException
from utils.database import execute_query_json
from models.pais import Pais

async def get_all_paises():
    sql = "SELECT * FROM PAIS"
    try:
        return await execute_query_json(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_one_pais(id: int):
    sql = "SELECT * FROM PAIS WHERE ID = :id"
    try:
        result = await execute_query_json(sql, {"id": id})
        if not result:
            raise HTTPException(status_code=404, detail="País no encontrado")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def create_pais(data: Pais):
    sql = "INSERT INTO PAIS (NOMBRE) VALUES (:nombre)"
    try:
        await execute_query_json(sql, {"nombre": data.nombre}, needs_commit=True)
        result = await execute_query_json(
            "SELECT * FROM PAIS ORDER BY ID DESC FETCH FIRST 1 ROWS ONLY"
        )
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_pais(id: int, data: Pais):
    sql = "UPDATE PAIS SET NOMBRE = :nombre WHERE ID = :id"
    params = {"nombre": data.nombre, "id": id}
    try:
        await execute_query_json(sql, params, needs_commit=True)
        result = await execute_query_json("SELECT * FROM PAIS WHERE ID=:id", {"id": id})
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_pais(id: int):
    sql = "DELETE FROM PAIS WHERE ID = :id"
    try:
        await execute_query_json(sql, {"id": id}, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
