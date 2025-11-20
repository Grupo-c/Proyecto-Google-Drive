from fastapi import HTTPException
from models.favoritos import Favorito
from utils.database import execute_query_json

async def get_one_favorito(id: int):
    sql = """
        SELECT 
            F.ID AS ID_FAVORITO,
            U.NOMBRE AS NOMBRE_USUARIO,
            C.NOMBRE AS NOMBRE_CARPETA,
            A.ID AS ID_ARCHIVO,
            A.NOMBRE AS NOMBRE_ARCHIVO,
            A.TIPO AS TIPO_ARCHIVO,
            CASE 
                WHEN A.TAMAÑO >= 1024 THEN CONCAT(ROUND(A.TAMAÑO / 1024.0, 2), ' GB')
                ELSE CONCAT(A.TAMAÑO, ' MB')
            END AS TAMAÑO_ARCHIVO,
            A.URL AS URL_ARCHIVO,

            F.FECHA_AGREGADO
        FROM GD.FAVORITOS F
        LEFT JOIN GD.USUARIO U ON F.ID_USUARIO = U.ID
        LEFT JOIN GD.CARPETA C ON F.ID_CARPETA = C.ID
        LEFT JOIN GD.ARCHIVO A ON F.ID_ARCHIVO = A.ID
        WHERE F.ID = ?
    """

    try:
        result = await execute_query_json(sql, [id])

        if len(result) == 0:
            raise HTTPException(status_code=404, detail="Favorito no encontrado")

        return result[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    
async def get_favoritos_by_usuario(id_usuario: int) -> list[Favorito]:
    sql = """
        SELECT 
            F.ID AS ID_FAVORITO,
            U.NOMBRE AS NOMBRE_USUARIO,
            C.NOMBRE AS NOMBRE_CARPETA,
            A.ID AS ID_ARCHIVO,
            A.NOMBRE AS NOMBRE_ARCHIVO,
            A.TIPO AS TIPO_ARCHIVO,
            CASE 
                WHEN A.TAMAÑO >= 1024 THEN CONCAT(ROUND(A.TAMAÑO / 1024.0, 2), ' GB')
                ELSE CONCAT(A.TAMAÑO, ' MB')
            END AS TAMAÑO_ARCHIVO,
            A.URL AS URL_ARCHIVO,

            F.FECHA_AGREGADO
        FROM GD.FAVORITOS F
        LEFT JOIN GD.USUARIO U ON F.ID_USUARIO = U.ID
        LEFT JOIN GD.CARPETA C ON F.ID_CARPETA = C.ID
        LEFT JOIN GD.ARCHIVO A ON F.ID_ARCHIVO = A.ID
        WHERE F.ID_USUARIO = ?
        ORDER BY F.FECHA_AGREGADO DESC
    """

    try:
        result = await execute_query_json(sql, [id_usuario])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    
async def create_favorito(favorito: Favorito) -> Favorito:
    sql = """
        INSERT INTO GD.FAVORITOS (id_usuario, id_carpeta, id_archivo, fecha_agregado)
        VALUES (?, ?, ?, ?)
    """
    params = [
        favorito.id_usuario,
        favorito.id_carpeta,
        favorito.id_archivo,
        favorito.fecha_agregado
    ]
    try:
        await execute_query_json(sql, params, needs_commit=True)
        sql_find = """
            SELECT TOP 1 *
            FROM GD.FAVORITOS
            WHERE id_usuario = ?
              AND id_carpeta = ?
              AND id_archivo = ?
              AND fecha_agregado = ?
            ORDER BY ID DESC
        """

        result = await execute_query_json(sql_find, params)

        return result[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    

async def delete_favorito(id_favorito: int) -> None:
    sql = "DELETE FROM GD.FAVORITOS WHERE id = ?"
    try:
        await execute_query_json(sql, [id_favorito], needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
async def update_favorito(favorito: Favorito) -> Favorito:
    data = favorito.model_dump(exclude_none=True)

    if "id_favorito" in data:
        data.pop("id_favorito")

    if "fecha" in data:
        data["fecha_agregado"] = data.pop("fecha")

    keys = list(data.keys())
    set_vars = " = ?, ".join(keys) + " = ?"

    sql = f"UPDATE GD.FAVORITOS SET {set_vars} WHERE ID = ?"
    params = [data[k] for k in keys] + [favorito.id_favorito]

    try:
        await execute_query_json(sql, params, needs_commit=True)

        sql_find = "SELECT * FROM GD.FAVORITOS WHERE ID = ?"
        result = await execute_query_json(sql_find, [favorito.id_favorito])

        return result[0] if result else None

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")