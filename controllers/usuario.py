from fastapi import HTTPException
import json
import logging

from utils.database import execute_query_json
from models.usuario import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_one_user(id: int) -> User:
    sql = """
        SELECT id, pais_id, correo, nombre, apellido, foto
        FROM usuario
        WHERE id = ?
    """

    try:
        result = await execute_query_json(sql, params=[id])
        data = json.loads(result)

        if len(data) == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def get_all_users() -> list[User]:
    sql = """
        SELECT id, pais_id, correo, nombre, apellido, foto
        FROM usuario
    """

    try:
        result = await execute_query_json(sql)
        return json.loads(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def delete_user(id: int) -> str:
    sql = """
        DELETE FROM usuario
        WHERE id = ?
    """

    try:
        await execute_query_json(sql, params=[id], needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def update_user(user: User) -> User:
    dict_user = user.model_dump(exclude_none=True)

    keys = list(dict_user.keys())
    keys.remove("id")
    set_vars = " = ?, ".join(keys) + " = ?"

    sql = f"""
        UPDATE usuario
        SET {set_vars}
        WHERE id = ?
    """

    params = [dict_user[k] for k in keys]
    params.append(user.id)

    try:
        await execute_query_json(sql, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    sql_find = """
        SELECT id, pais_id, correo, nombre, apellido, foto
        FROM usuario
        WHERE id = ?
    """

    try:
        result = await execute_query_json(sql_find, params=[user.id])
        data = json.loads(result)
        return data[0] if len(data) > 0 else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def create_user(user: User) -> User:
    sql = """
        INSERT INTO usuario (pais_id, correo, nombre, apellido, contraseña, foto)
        VALUES (?, ?, ?, ?, ?)
    """

    params = [
        user.pais_id,
        user.correo,
        user.nombre,
        user.apellido,
        user.contraseña,
        user.foto
        ]

    try:
        await execute_query_json(sql, params=params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    sql_find = """
        SELECT id, pais_id, correo, nombre, apellido
        FROM usuario
        WHERE correo = ?
    """

    try:
        result = await execute_query_json(sql_find, params=[user.correo])
        data = json.loads(result)
        return data[0] if len(data) > 0 else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
