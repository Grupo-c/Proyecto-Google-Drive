import json
from fastapi import HTTPException
from models.membresia import Membresia
from utils.database import execute_query_json

async def get_one_membership(id: int) -> Membresia:
    sql = """
        SELECT
            M.ID,
            M.NOMBRE,
            M.PRECIO 
        FROM MEMBRESIA M
        WHERE M.ID = :id
    """
    try:
        result = await execute_query_json(sql, {"id": id})
        if not result:
            raise HTTPException(status_code=404, detail="Membresía no encontrada")
        return Membresia(**result[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e
