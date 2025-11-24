from fastapi import HTTPException
from models.unidad import Unidad
from utils.database import execute_query_json

async def get_one_unidad(id: int) -> Unidad:
    sql = """
        SELECT 
            u.id,
            u.capacidad_total,
            u.capacidad_actual,
            u.id_membresia,
            u.fecha_compra,
            u.fecha_expiracion,
            us.nombre AS nombre_usuario
        FROM GD.UNIDAD u
        LEFT JOIN GD.USUARIO us ON u.id_usuario = us.id
        WHERE u.id = :id
    """
    try:
        result = await execute_query_json(sql, {"id": id})
        if len(result) == 0:
            raise HTTPException(status_code=404, detail="Unidad no encontrada")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_unidades() -> list[Unidad]:
    sql = """
        SELECT 
            u.id,
            u.capacidad_total,
            u.capacidad_actual,
            u.id_membresia,
            u.fecha_compra,
            u.fecha_expiracion,
            us.nombre AS nombre_usuario
        FROM GD.UNIDAD u
        LEFT JOIN GD.USUARIO us ON u.id_usuario = us.id
    """
    try:
        return await execute_query_json(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def create_unidad(unidad: Unidad) -> Unidad:
    sql = """
        INSERT INTO GD.UNIDAD 
        (id_usuario, capacidad_total, capacidad_actual, id_membresia, fecha_compra, fecha_expiracion)
        VALUES (:id_usuario, :cap_total, :cap_actual, :membresia, :f_compra, :f_exp)
    """
    params = {
        "id_usuario": unidad.id_usuario,
        "cap_total": unidad.capacidad_total,
        "cap_actual": unidad.capacidad_actual,
        "membresia": unidad.id_membresia,
        "f_compra": unidad.fecha_compra,
        "f_exp": unidad.fecha_expiracion
    }

    try:
        await execute_query_json(sql, params, needs_commit=True)

        # Oracle usa ROWNUM para obtener el último registro
        sql_find = """
            SELECT * FROM (
                SELECT u.*, us.nombre AS nombre_usuario
                FROM GD.UNIDAD u
                LEFT JOIN GD.USUARIO us ON u.id_usuario = us.id
                WHERE u.id_usuario = :id_usuario
                ORDER BY u.id DESC
            ) WHERE ROWNUM = 1
        """
        result = await execute_query_json(sql_find, {"id_usuario": unidad.id_usuario})
        return result[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_unidad(unidad: Unidad) -> Unidad:
    data = unidad.model_dump(exclude_none=True)

    if "id" not in data:
        raise HTTPException(status_code=400, detail="Id requerido para actualizar")

    fields = [f"{k} = :{k}" for k in data.keys() if k != "id"]

    sql = f"UPDATE GD.UNIDAD SET {', '.join(fields)} WHERE id = :id"

    try:
        await execute_query_json(sql, data, needs_commit=True)

        sql_find = """
            SELECT 
                u.*, 
                us.nombre AS nombre_usuario
            FROM GD.UNIDAD u
            LEFT JOIN GD.USUARIO us ON u.id_usuario = us.id
            WHERE u.id = :id
        """
        result = await execute_query_json(sql_find, {"id": unidad.id})
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_unidad(id: int) -> str:
    sql = "DELETE FROM GD.UNIDAD WHERE id = :id"
    try:
        await execute_query_json(sql, {"id": id}, needs_commit=True)
        return "DELETED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
