from fastapi import HTTPException
import logging
from typing import List, Optional

from models.spam import Spam
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_one_spam(id_spam: int) -> Optional[dict]:
    sql = """
        SELECT
            S.ID,
            S.ID_USUARIO,
            S.ID_ARCHIVO,
            S.ID_CARPETA,
            S.FECHA,
            U.NOMBRE AS NOMBRE_USUARIO,
            A.NOMBRE AS NOMBRE_ARCHIVO,
            C.NOMBRE AS NOMBRE_CARPETA
        FROM SPAM S
        LEFT JOIN USUARIO U ON S.ID_USUARIO = U.ID
        LEFT JOIN ARCHIVO A ON S.ID_ARCHIVO = A.ID
        LEFT JOIN CARPETA C ON S.ID_CARPETA = C.ID
        WHERE S.ID = :id
    """
    try:
        result = await execute_query_json(sql, {"id": id_spam})
        if not result:
            raise HTTPException(status_code=404, detail="Spam no encontrado")
        return result[0]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener spam {id_spam}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e


async def get_spam_by_usuario(id_usuario: int) -> List[dict]:
    sql = """
        SELECT
            S.ID,
            S.ID_USUARIO,
            S.ID_ARCHIVO,
            S.ID_CARPETA,
            S.FECHA,
            A.NOMBRE AS NOMBRE_ARCHIVO,
            C.NOMBRE AS NOMBRE_CARPETA
        FROM SPAM S
        LEFT JOIN ARCHIVO A ON S.ID_ARCHIVO = A.ID
        LEFT JOIN CARPETA C ON S.ID_CARPETA = C.ID
        WHERE S.ID_USUARIO = :id_usuario
        ORDER BY S.FECHA DESC
    """
    try:
        return await execute_query_json(sql, {"id_usuario": id_usuario})
    except Exception as e:
        logger.error(f"Error al listar spam del usuario {id_usuario}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e


async def create_spam(spam: Spam) -> dict:
    sql = """
        INSERT INTO SPAM (ID_USUARIO, ID_ARCHIVO, ID_CARPETA, FECHA)
        VALUES (:id_usuario, :id_archivo, :id_carpeta, :fecha)
    """

    params = {
        "id_usuario": spam.id_usuario,
        "id_archivo": spam.id_archivo,
        "id_carpeta": spam.id_carpeta,
        "fecha": spam.fecha,
    }

    try:
        await execute_query_json(sql, params, needs_commit=True)

        # Obtener el último insertado para el usuario (mejor recuperar por combinación única si existe)
        sql_find = """
            SELECT * FROM SPAM
            WHERE ID_USUARIO = :id_usuario
              AND ID_ARCHIVO = :id_archivo
              AND ID_CARPETA = :id_carpeta
              AND FECHA = :fecha
            ORDER BY ID DESC
            FETCH FIRST 1 ROW ONLY
        """
        result = await execute_query_json(sql_find, params)
        return result[0] if result else {}
    except Exception as e:
        logger.error(f"Error al crear spam: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e


async def delete_spam(id_spam: int) -> None:
    sql = "DELETE FROM SPAM WHERE ID = :id"
    try:
        await execute_query_json(sql, {"id": id_spam}, needs_commit=True)
    except Exception as e:
        logger.error(f"Error al eliminar spam {id_spam}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e
