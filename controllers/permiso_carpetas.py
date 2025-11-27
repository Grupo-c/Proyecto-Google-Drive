from fastapi import HTTPException
import logging
from typing import List

from models.permiso_carpeta import FoldersPermiso
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
