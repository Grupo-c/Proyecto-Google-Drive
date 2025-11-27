from fastapi import HTTPException
import logging
from typing import List

from models.permiso import Permiso, ArchivosPermiso, FoldersPermiso
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


# ARCHIVO_PERMISO helpers
async def add_permiso_archivo(data: ArchivosPermiso) -> dict:
    sql = "INSERT INTO ARCHIVO_PERMISO (ID_ARCHIVO, ID_PERMISO) VALUES (:id_archivo, :id_permiso)"
    params = {"id_archivo": data.id_archivo, "id_permiso": data.id_permiso}
    try:
        await execute_query_json(sql, params, needs_commit=True)
    except Exception as e:
        logger.error(f"Error al asignar permiso a archivo: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e

    sql_find = """
        SELECT AP.ID, AP.ID_ARCHIVO, AP.ID_PERMISO, P.NOMBRE AS NOMBRE_PERMISO
        FROM ARCHIVO_PERMISO AP
        LEFT JOIN PERMISOS P ON AP.ID_PERMISO = P.ID
        WHERE AP.ID_ARCHIVO = :id_archivo AND AP.ID_PERMISO = :id_permiso
        ORDER BY AP.ID DESC
        FETCH FIRST 1 ROW ONLY
    """
    try:
        result = await execute_query_json(sql_find, params)
        return result[0] if result else {}
    except Exception as e:
        logger.error(f"Error al recuperar permiso de archivo asignado: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e


async def list_permisos_archivo(id_archivo: int) -> List[dict]:
    sql = """
        SELECT AP.ID, AP.ID_ARCHIVO, AP.ID_PERMISO, P.NOMBRE AS NOMBRE_PERMISO
        FROM ARCHIVO_PERMISO AP
        LEFT JOIN PERMISOS P ON AP.ID_PERMISO = P.ID
        WHERE AP.ID_ARCHIVO = :id_archivo
    """
    try:
        return await execute_query_json(sql, {"id_archivo": id_archivo})
    except Exception as e:
        logger.error(f"Error al listar permisos de archivo {id_archivo}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e


async def remove_permiso_archivo(id: int) -> str:
    sql = "DELETE FROM ARCHIVO_PERMISO WHERE ID = :id"
    try:
        await execute_query_json(sql, {"id": id}, needs_commit=True)
        return "DELETED"
    except Exception as e:
        logger.error(f"Error al eliminar permiso archivo {id}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e


# CARPETA_PERMISO helpers
async def add_permiso_carpeta(data: FoldersPermiso) -> dict:
    sql = "INSERT INTO CARPETA_PERMISO (ID_CARPETA, ID_PERMISO) VALUES (:id_carpeta, :id_permiso)"
    params = {"id_carpeta": data.id_folder, "id_permiso": data.id_permiso}
    try:
        await execute_query_json(sql, params, needs_commit=True)
    except Exception as e:
        logger.error(f"Error al asignar permiso a carpeta: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e

    sql_find = """
        SELECT CP.ID, CP.ID_CARPETA, CP.ID_PERMISO, P.NOMBRE AS NOMBRE_PERMISO
        FROM CARPETA_PERMISO CP
        LEFT JOIN PERMISOS P ON CP.ID_PERMISO = P.ID
        WHERE CP.ID_CARPETA = :id_carpeta AND CP.ID_PERMISO = :id_permiso
        ORDER BY CP.ID DESC
        FETCH FIRST 1 ROW ONLY
    """
    try:
        result = await execute_query_json(sql_find, params)
        return result[0] if result else {}
    except Exception as e:
        logger.error(f"Error al recuperar permiso de carpeta asignado: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e


async def list_permisos_carpeta(id_carpeta: int) -> List[dict]:
    sql = """
        SELECT CP.ID, CP.ID_CARPETA, CP.ID_PERMISO, P.NOMBRE AS NOMBRE_PERMISO
        FROM CARPETA_PERMISO CP
        LEFT JOIN PERMISOS P ON CP.ID_PERMISO = P.ID
        WHERE CP.ID_CARPETA = :id_carpeta
    """
    try:
        return await execute_query_json(sql, {"id_carpeta": id_carpeta})
    except Exception as e:
        logger.error(f"Error al listar permisos de carpeta {id_carpeta}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e


async def remove_permiso_carpeta(id: int) -> str:
    sql = "DELETE FROM CARPETA_PERMISO WHERE ID = :id"
    try:
        await execute_query_json(sql, {"id": id}, needs_commit=True)
        return "DELETED"
    except Exception as e:
        logger.error(f"Error al eliminar permiso carpeta {id}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e
