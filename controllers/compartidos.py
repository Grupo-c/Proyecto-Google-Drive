import json
from fastapi import HTTPException
from models.compartidos import Compartido
from utils.database import execute_query_json

# Obtener todos los compartidos de un usuario.
async def get_shared_by_user(id_usuario: int) -> list:
    sql = """
        SELECT 
            CO.ID,
            CO.ID_USUARIO,
            U.NOMBRE AS NOMBRE_USUARIO,
            CO.ID_ARCHIVO,
            A.NOMBRE AS NOMBRE_ARCHIVO,
            CO.ID_CARPETA,
            CA.NOMBRE AS NOMBRE_CARPETA,
            CO.ID_PERMISO,
            P.NOMBRE AS NOMBRE_PERMISO
        FROM GD.COMPARTIDOS CO
        LEFT JOIN GD.USUARIO U ON CO.ID_USUARIO = U.ID
        LEFT JOIN GD.ARCHIVO A ON CO.ID_ARCHIVO = A.ID
        LEFT JOIN GD.CARPETA CA ON CO.ID_CARPETA = CA.ID
        LEFT JOIN GD.PERMISOS P ON CO.ID_PERMISO = P.ID
        WHERE CO.ID_USUARIO = :id_usuario
    """
    try:
        result = await execute_query_json(sql, {"id_usuario": id_usuario})
        if not result:
            raise HTTPException(status_code=404, detail="No hay compartidos para este usuario")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Obtener un compartido por ID
async def get_one_shared(id: int) -> dict:
    sql = """
        SELECT 
            CO.ID,
            CO.ID_USUARIO,
            CO.ID_ARCHIVO,
            CO.ID_CARPETA,
            CO.ID_PERMISO
        FROM GD.COMPARTIDOS CO
        WHERE CO.ID = :id
    """
    try:
        result = await execute_query_json(sql, {"id": id})
        if not result:
            raise HTTPException(status_code=404, detail="Compartido no encontrado")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Crear un compartido
async def create_shared(compartido: Compartido) -> dict:
    sql = """
        INSERT INTO GD.COMPARTIDOS (ID_USUARIO, ID_ARCHIVO, ID_CARPETA, ID_PERMISO)
        VALUES (:id_usuario, :id_archivo, :id_carpeta, :id_permiso)
    """
    params = {
        "id_usuario": compartido.id_usuario,
        "id_archivo": compartido.id_archivo,
        "id_carpeta": compartido.id_carpeta,
        "id_permiso": compartido.id_permiso
    }
    try:
        await execute_query_json(sql, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    sql_find = """
        SELECT ID, ID_USUARIO, ID_ARCHIVO, ID_CARPETA, ID_PERMISO
        FROM GD.COMPARTIDOS
        WHERE ID_USUARIO = :id_usuario AND ID_PERMISO = :id_permiso
        ORDER BY ID DESC
    """
    try:
        result = await execute_query_json(sql_find, {
            "id_usuario": compartido.id_usuario,
            "id_permiso": compartido.id_permiso
        })
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Actualizar un compartido
async def update_shared(compartido: Compartido) -> dict:
    data = compartido.model_dump(exclude_none=True)
    keys = [k for k in data if k != "id"]

    if not keys:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")

    set_clause = ", ".join([f"{k} = :{k}" for k in keys])
    sql = f"UPDATE GD.COMPARTIDOS SET {set_clause} WHERE ID = :id"

    params = {k: data[k] for k in keys}
    params["id"] = compartido.id

    try:
        await execute_query_json(sql, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    sql_find = """
        SELECT ID, ID_USUARIO, ID_ARCHIVO, ID_CARPETA, ID_PERMISO
        FROM GD.COMPARTIDOS
        WHERE ID = :id
    """
    try:
        result = await execute_query_json(sql_find, {"id": compartido.id})
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Eliminar un compartido
async def delete_shared(id: int) -> str:
    sql = "DELETE FROM GD.COMPARTIDOS WHERE ID = :id"
    try:
        await execute_query_json(sql, {"id": id}, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
