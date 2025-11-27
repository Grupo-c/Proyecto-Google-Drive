from fastapi import HTTPException
import json
import logging

from utils.database import execute_query_json
from models.usuario import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# GET ONE USER
async def get_one_user(id: int) -> User:
    sql = """
        SELECT 
            U.ID,
            U.NOMBRE,
            U.APELLIDO,
            U.CORREO,
            U.FOTO,
            P.NOMBRE AS NOMBRE_PAIS
        FROM GD.USUARIO U
        LEFT JOIN GD.PAIS P ON U.ID_PAIS = P.ID
        WHERE U.ID = :id
    """

    try:
        result = await execute_query_json(sql, params={"id": id})

        if len(result) == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return result[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")



# GET ALL USERS
async def get_all_users() -> list[User]:
    sql = """
        SELECT 
            U.ID,
            U.NOMBRE,
            U.APELLIDO,
            U.CORREO,
            U.FOTO,
            P.NOMBRE AS NOMBRE_PAIS
        FROM GD.USUARIO U
        LEFT JOIN GD.PAIS P ON U.ID_PAIS = P.ID
    """

    try:
        return await execute_query_json(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

# DELETE USER
async def delete_user(id: int) -> str:
    sql = """
        DELETE FROM GD.USUARIO
        WHERE ID = :id
    """

    try:
        await execute_query_json(sql, params={"id": id}, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")



# UPDATE USER
async def update_user(user: User) -> User:
    dict_user = user.model_dump(exclude_none=True)

    keys = list(dict_user.keys())
    keys.remove("id")

    set_vars = ", ".join([f"{k} = :{i+1}" for i, k in enumerate(keys)])

    sql = f"""
        UPDATE GD.USUARIO
        SET {set_vars}
        WHERE ID = :{len(keys)+1}
    """

    params = [dict_user[k] for k in keys]
    params.append(user.id)

    try:
        await execute_query_json(sql, params=params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    sql_find = """
        SELECT id, id_pais, correo, nombre, apellido, foto
        FROM GD.USUARIO
        WHERE id = :id
    """

    try:
        result = await execute_query_json(sql_find, params={"id": user.id})
        return result[0] if len(result) > 0 else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def create_user(user: User) -> User:
    sql = """
        INSERT INTO GD.USUARIO (ID_PAIS, CORREO, NOMBRE, APELLIDO, FOTO)
        VALUES (:id_pais, :correo, :nombre, :apellido, :foto)
    """
    params = [
        user.id_pais,
        user.correo,
        user.nombre,
        user.apellido,
        user.foto
    ]

    try:
        await execute_query_json(sql, params=params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    # Buscar usuario recién creado
    sql_find = """
        SELECT id, id_pais, correo, nombre, apellido
        FROM GD.USUARIO
        WHERE correo = :correo
    """

    try:
        result = await execute_query_json(sql_find, params={"correo": user.correo})
        return result[0] if len(result) > 0 else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
