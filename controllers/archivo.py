import json
from fastapi import HTTPException
from models.archivo import Archivo
from utils.database import execute_query_json


async def get_one_file(id: int) -> Archivo:
    sql = """
        SELECT 
            A.ID, 
            U.NOMBRE AS NOMBRE_USUARIO, 
            C.NOMBRE AS NOMBRE_CARPETA,
            A.NOMBRE, 
            A.TIPO, 
            CASE 
                WHEN A.TAMANO >= 1024 THEN ROUND(A.TAMANO / 1024, 2) || ' GB'
                ELSE A.TAMANO || ' MB'
            END AS TAMANO,
            A.FECHA_CREACION,
            A.FECHA_MODIFICACION, 
            A.URL,
            A.VISIBILIDAD
        FROM ARCHIVO A
        LEFT JOIN USUARIO U ON A.ID_USUARIO = U.ID
        LEFT JOIN CARPETA C ON A.ID_CARPETA = C.ID
        WHERE A.ID = :id
    """
    try:
        result = await execute_query_json(sql, {"id": id})
        if not result:
            raise HTTPException(status_code=404, detail="Archivo no encontrado")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e



async def get_all_files() -> list[Archivo]:
    sql = """
        SELECT 
            A.ID, 
            U.NOMBRE AS NOMBRE_USUARIO, 
            C.NOMBRE AS NOMBRE_CARPETA,
            A.NOMBRE, 
            A.TIPO, 
            CASE 
                WHEN A.TAMANO >= 1024 THEN ROUND(A.TAMANO / 1024, 2) || ' GB'
                ELSE A.TAMANO || ' MB'
            END AS TAMANO,
            A.FECHA_CREACION,
            A.FECHA_MODIFICACION, 
            A.URL,
            A.VISIBILIDAD
        FROM ARCHIVO A
        LEFT JOIN USUARIO U ON A.ID_USUARIO = U.ID
        LEFT JOIN CARPETA C ON A.ID_CARPETA = C.ID
    """
    try:
        return await execute_query_json(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e


async def delete_file(id: int) -> str:
    try:
        # Borrar hijos primero
        sql_cleanup = """
        BEGIN
            DELETE FROM FAVORITOS WHERE ID_ARCHIVO = :id;
            DELETE FROM SPAM WHERE ID_ARCHIVO = :id;
            DELETE FROM COMPARTIDOS WHERE ID_ARCHIVO = :id;
        END;
        """
        await execute_query_json(sql_cleanup, {"id": id}, needs_commit=True)

        # Borrar archivo
        sql_delete = "DELETE FROM ARCHIVO WHERE ID = :id"
        await execute_query_json(sql_delete, {"id": id}, needs_commit=True)

        return f"Archivo con id {id} eliminado correctamente."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e


async def create_file(file: Archivo) -> Archivo:
    sql = """
        INSERT INTO ARCHIVO 
            (ID_USUARIO, ID_CARPETA, ID_ICONO, NOMBRE, TIPO, TAMANO, URL, VISIBILIDAD)
        VALUES 
            (:id_usuario, :id_carpeta, :id_icono, :nombre, :tipo, :tamano, :url, :visibilidad)
    """
    params = {
        "id_usuario": file.id_usuario,
        "id_carpeta": file.id_carpeta,
        "id_icono": file.id_icono,
        "nombre": file.nombre,
        "tipo": file.tipo,
        "tamano": file.tamaño,
        "url": file.url,
        "visibilidad": file.visibilidad
    }
    try:
        await execute_query_json(sql, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e


    sql_find = "SELECT * FROM ARCHIVO WHERE URL = :url"
    try:
        result = await execute_query_json(sql_find, {"url": file.url})
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e



async def update_file(file: Archivo) -> Archivo:
    data = file.model_dump(exclude_none=True)
    keys = [k for k in data if k != "id"]

    set_clause = ", ".join([f"{k} = :{k}" for k in keys])
    sql = f"UPDATE ARCHIVO SET {set_clause} WHERE ID = :id"
    params = {k: data[k] for k in keys}
    params["id"] = file.id

    try:
        await execute_query_json(sql, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e


    sql_find = "SELECT * FROM ARCHIVO WHERE ID = :id"
    try:
        result = await execute_query_json(sql_find, {"id": file.id})
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e
