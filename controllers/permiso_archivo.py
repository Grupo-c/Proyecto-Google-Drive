from fastapi import HTTPException
import logging
from typing import List

from models.permiso_archivo import ArchivosPermiso
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
