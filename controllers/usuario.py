from fastapi import HTTPException
import json
import logging

from utils.database import execute_query_json
from models.usuario import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_one_user(id: int) -> User:
    sql = """
        SELECT 
            U.ID AS id,
            U.NOMBRE AS nombre,
            U.APELLIDO AS apellido,
            U.CORREO AS correo,
            U.ID_PAIS AS id_pais,
            U.FOTO AS foto
        FROM GD.USUARIO U
        WHERE U.ID = :id
    """

    try:
        result = await execute_query_json(sql, params={"id": id})

        if not result:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return User(**result[0])  # ← validación correcta

    except Exception as e:
        logger.error(f"Error al obtener usuario con ID {id}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e


async def get_all_users() -> list[User]:
    sql = """
        SELECT 
            U.ID AS id,
            U.NOMBRE AS nombre,
            U.APELLIDO AS apellido,
            U.CORREO AS correo,
            U.ID_PAIS AS id_pais,
            U.FOTO AS foto
        FROM GD.USUARIO U
    """
    try:
        result = await execute_query_json(sql)
        
        return [User(**row) for row in result]

    except Exception as e:
        logger.error(f"Error al obtener todos los usuarios: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e


async def delete_user(id: int) -> str:
    sql = """
        DELETE FROM GD.USUARIO
        WHERE ID = :id
    """

    try:
        await execute_query_json(sql, params={"id": id}, needs_commit=True)
        return f"Usuario con id {id} eliminado correctamente."
    except Exception as e:
        logger.error(f"Error al eliminar usuario con ID {id}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e

async def update_user(user: User) -> User:
    dict_user = user.model_dump(exclude_none=True)

    keys = [k for k in dict_user if k != "id"]
    
    set_clause = ", ".join([f"{k} = :{k}" for k in keys])
    sql = f"""
        UPDATE GD.USUARIO
        SET {set_clause}
        WHERE ID = :id
    """
    params = {k: dict_user[k] for k in keys}
    params["id"] = user.id

    try:
        await execute_query_json(sql, params=params, needs_commit=True)
    except Exception as e:
        logger.error(f"Error al actualizar usuario con ID {user.id}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e


    sql_find = """
        SELECT id, id_pais, correo, nombre, apellido, foto
        FROM GD.USUARIO
        WHERE id = :id
    """

    try:
        result = await execute_query_json(sql_find, params={"id": user.id})
        return User(**result[0]) if result else None
    except Exception as e:
        logger.error(f"Error al buscar usuario actualizado con ID {user.id}: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e

async def create_user(user: User) -> User:
    sql = """
        INSERT INTO GD.USUARIO (ID_PAIS, CORREO, NOMBRE, APELLIDO, FOTO)
        VALUES (:id_pais, :correo, :nombre, :apellido, :foto)
    """
    params = {
        "id_pais": user.id_pais,
        "correo": user.correo,
        "nombre": user.nombre,
        "apellido": user.apellido,
        "foto": user.foto
    }
    try:
        await execute_query_json(sql, params=params, needs_commit=True)
    except Exception as e:
        logger.error(f"Error al crear usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e

    sql_find = """
        SELECT id, id_pais, correo, nombre, apellido, foto
        FROM GD.USUARIO
        WHERE correo = :correo
    """
    try:
        result = await execute_query_json(sql_find, params={"correo": user.correo})
        return User(**result[0]) if result else None
    except Exception as e:
        logger.error(f"Error al buscar usuario recién creado: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e