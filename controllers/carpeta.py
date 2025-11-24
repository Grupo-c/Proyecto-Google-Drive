from fastapi import HTTPException
from models.carpeta import Carpeta
from utils.database import execute_query_json

async def get_one_carpeta(id: int):
    sql = """
        SELECT 
            c.id,
            c.nombre,
            c.tamaño,
            c.fecha_creacion,
            c.fecha_modificacion,
            c.visibilidad,
            u.nombre AS nombre_usuario,
            cp.nombre AS carpeta_padre_nombre
        FROM GD.CARPETA c
        LEFT JOIN GD.USUARIO u ON c.id_usuario = u.id
        LEFT JOIN GD.CARPETA cp ON c.id_carpeta_padre = cp.id
        WHERE c.id = :id
    """
    try:
        result = await execute_query_json(sql, {"id": id})
        if not result:
            raise HTTPException(status_code=404, detail="Carpeta no encontrada")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_carpetas():
    sql = """
        SELECT 
            c.id,
            c.nombre,
            c.tamaño,
            c.fecha_creacion,
            c.fecha_modificacion,
            c.visibilidad,
            u.nombre AS nombre_usuario,
            cp.nombre AS carpeta_padre_nombre
        FROM GD.CARPETA c
        LEFT JOIN GD.USUARIO u ON c.id_usuario = u.id
        LEFT JOIN GD.CARPETA cp ON c.id_carpeta_padre = cp.id
    """
    try:
        return await execute_query_json(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def create_carpeta(carpeta: Carpeta):
    sql = """
        INSERT INTO GD.CARPETA (
            id_usuario, id_carpeta_padre, nombre, tamaño, 
            fecha_creacion, fecha_modificacion, visibilidad
        ) 
        VALUES (
            :id_usuario, :padre, :nombre, :tam, :f_crea, :f_mod, :vis
        )
    """
    params = {
        "id_usuario": carpeta.id_usuario,
        "padre": carpeta.id_carpeta_padre,
        "nombre": carpeta.nombre,
        "tam": carpeta.tamaño,
        "f_crea": carpeta.fecha_creacion,
        "f_mod": carpeta.fecha_modificacion,
        "vis": carpeta.visibilidad,
    }

    try:
        await execute_query_json(sql, params, needs_commit=True)

        sql_find = """
            SELECT * FROM (
                SELECT 
                    c.*, 
                    u.nombre AS nombre_usuario,
                    cp.nombre AS carpeta_padre_nombre
                FROM GD.CARPETA c
                LEFT JOIN GD.USUARIO u ON c.id_usuario = u.id
                LEFT JOIN GD.CARPETA cp ON c.id_carpeta_padre = cp.id
                WHERE c.nombre = :nombre AND c.id_usuario = :id_usuario
                ORDER BY c.id DESC
            )
            WHERE ROWNUM = 1
        """

        result = await execute_query_json(sql_find, {
            "nombre": carpeta.nombre,
            "id_usuario": carpeta.id_usuario
        })
        return result[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_carpeta(carpeta: Carpeta):
    data = carpeta.model_dump(exclude_none=True)

    if "id" not in data:
        raise HTTPException(status_code=400, detail="Id requerido para actualizar")

    fields = [f"{k} = :{k}" for k in data.keys() if k != "id"]

    sql = f"UPDATE GD.CARPETA SET {', '.join(fields)} WHERE id = :id"

    try:
        await execute_query_json(sql, data, needs_commit=True)

        sql_find = """
            SELECT 
                c.*, 
                u.nombre AS nombre_usuario,
                cp.nombre AS carpeta_padre_nombre
            FROM GD.CARPETA c
            LEFT JOIN GD.USUARIO u ON c.id_usuario = u.id
            LEFT JOIN GD.CARPETA cp ON c.id_carpeta_padre = cp.id
            WHERE c.id = :id
        """

        result = await execute_query_json(sql_find, {"id": carpeta.id})
        return result[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_carpeta(id: int):
    sql = "DELETE FROM GD.CARPETA WHERE id = :id"
    try:
        await execute_query_json(sql, {"id": id}, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
