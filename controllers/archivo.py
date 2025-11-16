import json
from fastapi import HTTPException
from models.archivo import Archivo
from utils.database import execute_query_json

async def get_one_file(id: int) -> Archivo:
    sql = """
        SELECT id, id_usuario, id_carpeta,
               nombre, tipo, tamaño, fecha_creacion,
               fecha_modificacion, url, visibilidad
        FROM GD.ARCHIVO
        WHERE id = ?
    """

    try:
        result = await execute_query_json(sql, [id])
        data = result

        if len(data) == 0:
            raise HTTPException(status_code=404, detail="Archivo no encontrado")

        return data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def get_all_files() -> list[Archivo]:
    sql = """
        SELECT id, id_usuario, id_carpeta,
               nombre, tipo, tamaño, fecha_creacion,
               fecha_modificacion, url, visibilidad
        FROM GD.ARCHIVO
    """

    try:
        result = await execute_query_json(sql)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def delete_file(id: int) -> str:
    sql = "DELETE FROM GD.ARCHIVO WHERE id = ?"

    try:
        await execute_query_json(sql, [id], needs_commit=True)
        return "DELETED"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def create_file(file: Archivo) -> Archivo:
    sql = """
        INSERT INTO archivo (id_usuario, id_carpeta, nombre, tipo, tamaño,
                             fecha_creacion, fecha_modificacion, url, visibilidad)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    params = [
        file.id_usuario,
        file.id_carpeta,
        file.nombre,
        file.tipo,
        file.tamaño,
        file.fecha_creacion,
        file.fecha_modificacion,
        file.url,
        file.visibilidad
    ]

    try:
        await execute_query_json(sql, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    sql_find = """
        SELECT id, id_usuario, id_carpeta,
               nombre, tipo, tamaño, fecha_creacion,
               fecha_modificacion, url, visibilidad
        FROM GD.ARCHIVO
        WHERE nombre = ? AND usuario_id = ?
    """

    try:
        result = await execute_query_json(sql_find, [file.nombre, file.id_propietario])
        return json.loads(result)[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def update_file(file: Archivo) -> Archivo:
    data = file.model_dump(exclude_none=True)

    keys = list(data.keys())
    keys.remove("id")

    set_vars = " = ?, ".join(keys) + " = ?"

    sql = f"""
        UPDATE GD.ARCHIVO
        SET {set_vars}
        WHERE id = ?
    """

    params = [data[k] for k in keys] + [file.id]

    try:
        await execute_query_json(sql, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    sql_find = """
        SELECT id, id_usuario,id_carpeta,
               nombre, tipo, tamaño, fecha_creacion,
               fecha_modificacion, url, visibilidad
        FROM GD.ARCHIVO
        WHERE id = ?
    """

    try:
        result = await execute_query_json(sql_find, [file.id])
        data = json.loads(result)
        return data[0] if len(data) else None

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")