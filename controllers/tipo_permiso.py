from fastapi import HTTPException
import logging
from typing import List

from models.tipo_permiso import Permiso
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_all_permisos() -> List[dict]:
    sql = """
        SELECT ID, NOMBRE, DESCRIPCION
        FROM PERMISOS
        ORDER BY ID
    """
    try:
        return await execute_query_json(sql)
    except Exception as e:
        logger.error(f"Error al obtener permisos: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e


async def get_one_permiso(id_permiso: int) -> dict:
    sql = """
        SELECT ID, NOMBRE, DESCRIPCION
        FROM PERMISOS
        WHERE ID = :id
    """
    try:
        result = await execute_query_json(sql, {"id": id_permiso})
        if not result:
            raise HTTPException(status_code=404, detail="Permiso no encontrado")
        return result[0]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener permiso {id_permiso}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e


async def create_permiso(permiso: Permiso) -> dict:
    sql = """
        INSERT INTO PERMISOS (NOMBRE, DESCRIPCION)
        VALUES (:nombre, :descripcion)
    """
    params = {"nombre": permiso.nombre, "descripcion": permiso.descripcion}
    try:
        await execute_query_json(sql, params, needs_commit=True)
    except Exception as e:
        logger.error(f"Error al crear permiso: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e

    sql_find = """
        SELECT ID, NOMBRE, DESCRIPCION
        FROM PERMISOS
        WHERE NOMBRE = :nombre AND (DESCRIPCION = :descripcion OR (:descripcion IS NULL AND DESCRIPCION IS NULL))
        ORDER BY ID DESC
        FETCH FIRST 1 ROW ONLY
    """
    try:
        result = await execute_query_json(sql_find, params)
        return result[0] if result else {}
    except Exception as e:
        logger.error(f"Error al buscar permiso creado: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e


async def update_permiso(permiso: Permiso) -> dict:
    data = permiso.model_dump(exclude_none=True)
    # Expect id field name possibly 'id_permiso' in model
    pid = data.get("id") or data.get("id_permiso") or data.get("ID")
    if not pid:
        raise HTTPException(status_code=400, detail="ID de permiso es requerido")

    keys = [k for k in data if k.lower() not in ("id", "id_permiso", "id_permiso")] 
    if not keys:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")

    set_clause = ", ".join([f"{k.upper()} = :{k}" for k in keys])
    sql = f"UPDATE PERMISOS SET {set_clause} WHERE ID = :id"

    params = {k: data[k] for k in keys}
    params["id"] = pid

    try:
        await execute_query_json(sql, params, needs_commit=True)
    except Exception as e:
        logger.error(f"Error al actualizar permiso {pid}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e

    try:
        return await get_one_permiso(pid)
    except Exception:
        return {}


async def delete_permiso(id_permiso: int) -> str:
    sql = "DELETE FROM PERMISOS WHERE ID = :id"
    try:
        await execute_query_json(sql, {"id": id_permiso}, needs_commit=True)
        return "DELETED"
    except Exception as e:
        logger.error(f"Error al eliminar permiso {id_permiso}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e
