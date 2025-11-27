from fastapi import HTTPException
from utils.database import execute_query_json
from models.membresia import Membresia

async def get_all_membresias():
    sql = "SELECT * FROM MEMBRESIA"
    try:
        return await execute_query_json(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def get_one_membresia(id: int):
    sql = "SELECT * FROM MEMBRESIA WHERE ID = :id"
    try:
        result = await execute_query_json(sql, {"id": id})
        if not result:
            raise HTTPException(status_code=404, detail="Membresía no encontrada")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def create_membresia(data: Membresia):
    sql = """
        INSERT INTO MEMBRESIA (NOMBRE, PRECIO)
        VALUES (:nombre, :precio)
    """
    params = {
        "nombre": data.nombre,
        "precio": data.precio
    }
    try:
        await execute_query_json(sql, params, needs_commit=True)

        result = await execute_query_json(
            "SELECT * FROM MEMBRESIA ORDER BY ID DESC FETCH FIRST 1 ROWS ONLY"
        )
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def update_membresia(id: int, data: Membresia):
    sql = """
        UPDATE MEMBRESIA SET 
            NOMBRE = :nombre,
            PRECIO = :precio
        WHERE ID = :id
    """
    params = {
        "id": id,
        "nombre": data.nombre,
        "precio": data.precio
    }
    try:
        await execute_query_json(sql, params, needs_commit=True)

        result = await execute_query_json("SELECT * FROM MEMBRESIA WHERE ID = :id", {"id": id})
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def delete_membresia(id: int):
    sql = "DELETE FROM MEMBRESIA WHERE ID = :id"
    try:
        await execute_query_json(sql, {"id": id}, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
