import json
from fastapi import HTTPException
from models.descargas import Descarga
from utils.database import execute_query_json

# Obtener todas las descargas de un usuario
async def get_downloads_by_user(id_usuario: int) -> list:
    sql = """
        SELECT 
            D.ID,
            D.ID_USUARIO,
            U.NOMBRE AS NOMBRE_USUARIO,
            D.ID_CARPETA,
            CA.NOMBRE AS NOMBRE_CARPETA,
            D.ID_ARCHIVO,
            A.NOMBRE AS NOMBRE_ARCHIVO,
            D.DESTINO_DESCARGA,
            D.FECHA_DESCARGA,
            D.FECHA_ACTUALIZACION
        FROM GD.DESCARGAS D
        LEFT JOIN GD.USUARIO U ON D.ID_USUARIO = U.ID
        LEFT JOIN GD.CARPETA CA ON D.ID_CARPETA = CA.ID
        LEFT JOIN GD.ARCHIVO A ON D.ID_ARCHIVO = A.ID
        WHERE D.ID_USUARIO = :id_usuario
        ORDER BY D.FECHA_DESCARGA DESC
    """
    try:
        result = await execute_query_json(sql, {"id_usuario": id_usuario})
        if not result:
            raise HTTPException(status_code=404, detail="No hay descargas para este usuario")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Obtener todas las descargas de un archivo
async def get_downloads_by_file(id_archivo: int) -> list:
    sql = """
        SELECT 
            D.ID,
            D.ID_USUARIO,
            U.NOMBRE AS NOMBRE_USUARIO,
            D.ID_CARPETA,
            D.ID_ARCHIVO,
            D.DESTINO_DESCARGA,
            D.FECHA_DESCARGA,
            D.FECHA_ACTUALIZACION
        FROM GD.DESCARGAS D
        LEFT JOIN GD.USUARIO U ON D.ID_USUARIO = U.ID
        WHERE D.ID_ARCHIVO = :id_archivo
        ORDER BY D.FECHA_DESCARGA DESC
    """
    try:
        result = await execute_query_json(sql, {"id_archivo": id_archivo})
        if not result:
            raise HTTPException(status_code=404, detail="No hay descargas para este archivo")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Obtener una descarga por ID
async def get_one_download(id: int) -> dict:
    sql = """
        SELECT 
            ID,
            ID_USUARIO,
            ID_CARPETA,
            ID_ARCHIVO,
            DESTINO_DESCARGA,
            FECHA_DESCARGA,
            FECHA_ACTUALIZACION
        FROM GD.DESCARGAS
        WHERE ID = :id
    """
    try:
        result = await execute_query_json(sql, {"id": id})
        if not result:
            raise HTTPException(status_code=404, detail="Descarga no encontrada")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Crear una descarga
async def create_download(descarga: Descarga) -> dict:
    sql = """
        INSERT INTO GD.DESCARGAS (ID_USUARIO, ID_CARPETA, ID_ARCHIVO, DESTINO_DESCARGA, FECHA_DESCARGA)
        VALUES (:id_usuario, :id_carpeta, :id_archivo, :destino_descarga, SYSDATE)
    """
    params = {
        "id_usuario": descarga.id_usuario,
        "id_carpeta": descarga.id_carpeta,
        "id_archivo": descarga.id_archivo,
        "destino_descarga": descarga.destino_descarga
    }
    try:
        await execute_query_json(sql, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    sql_find = """
        SELECT ID, ID_USUARIO, ID_CARPETA, ID_ARCHIVO, DESTINO_DESCARGA, FECHA_DESCARGA, FECHA_ACTUALIZACION
        FROM GD.DESCARGAS
        WHERE ID_USUARIO = :id_usuario AND ID_ARCHIVO = :id_archivo
        ORDER BY FECHA_DESCARGA DESC
    """
    try:
        result = await execute_query_json(sql_find, {
            "id_usuario": descarga.id_usuario,
            "id_archivo": descarga.id_archivo
        })
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Actualizar una descarga
async def update_download(descarga: Descarga) -> dict:
    data = descarga.model_dump(exclude_none=True)
    keys = [k for k in data if k != "id"]

    if not keys:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")

    set_clause = ", ".join([f"{k} = :{k}" for k in keys])
    sql = f"UPDATE GD.DESCARGAS SET {set_clause} WHERE ID = :id"

    params = {k: data[k] for k in keys}
    params["id"] = descarga.id

    try:
        await execute_query_json(sql, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    sql_find = """
        SELECT ID, ID_USUARIO, ID_CARPETA, ID_ARCHIVO, DESTINO_DESCARGA, FECHA_DESCARGA, FECHA_ACTUALIZACION
        FROM GD.DESCARGAS
        WHERE ID = :id
    """
    try:
        result = await execute_query_json(sql_find, {"id": descarga.id})
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Eliminar una descarga
async def delete_download(id: int) -> str:
    sql = "DELETE FROM GD.DESCARGAS WHERE ID = :id"
    try:
        await execute_query_json(sql, {"id": id}, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
