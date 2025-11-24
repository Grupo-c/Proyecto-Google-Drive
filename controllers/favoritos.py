from fastapi import HTTPException
from models.favoritos import Favorito, FavoritoUpdate
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
                WHEN A.TAMANO >= 1024 THEN ROUND(A.TAMANO / 1024.0, 2) || ' GB'
                ELSE A.TAMANO || ' MB'
            END AS TAMANO_ARCHIVO,
            A.URL AS URL_ARCHIVO,
            F.FECHA_AGREGADO
        FROM FAVORITOS F
        LEFT JOIN USUARIO U ON F.ID_USUARIO = U.ID
        LEFT JOIN CARPETA C ON F.ID_CARPETA = C.ID
        LEFT JOIN ARCHIVO A ON F.ID_ARCHIVO = A.ID
        WHERE F.ID = :1
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
                WHEN A.TAMANO >= 1024 THEN ROUND(A.TAMANO / 1024.0, 2) || ' GB'
                ELSE A.TAMANO || ' MB'
            END AS TAMANO_ARCHIVO,
            A.URL AS URL_ARCHIVO,
            F.FECHA_AGREGADO
        FROM FAVORITOS F
        LEFT JOIN USUARIO U ON F.ID_USUARIO = U.ID
        LEFT JOIN CARPETA C ON F.ID_CARPETA = C.ID
        LEFT JOIN ARCHIVO A ON F.ID_ARCHIVO = A.ID
        WHERE F.ID_USUARIO = :1
        ORDER BY F.FECHA_AGREGADO DESC
    """

    try:
        return await execute_query_json(sql, [id_usuario])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def create_favorito(favorito: Favorito) -> Favorito:

    sql = """
        INSERT INTO FAVORITOS (id_usuario, id_carpeta, id_archivo, fecha_agregado)
        VALUES (:1, :2, :3, :4)
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
            SELECT *
            FROM FAVORITOS
            WHERE id_usuario = :1
              AND id_carpeta = :2
              AND id_archivo = :3
              AND fecha_agregado = :4
            ORDER BY ID DESC
            FETCH FIRST 1 ROW ONLY
        """

        result = await execute_query_json(sql_find, params)

        return result[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")



async def delete_favorito(id_favorito: int) -> None:
    sql = "DELETE FROM FAVORITOS WHERE id = :1"

    try:
        await execute_query_json(sql, [id_favorito], needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def update_favorito(id: int, data: FavoritoUpdate) -> Favorito:
    update_data = data.model_dump(exclude_none=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No se enviaron campos para actualizar")

    set_clauses = ", ".join([f"{k.upper()} = :{k}" for k in update_data.keys()])
    sql = f"UPDATE FAVORITOS SET {set_clauses} WHERE ID = :id"

    params = {**update_data, "id": id}

    try:
        await execute_query_json(sql, params, needs_commit=True)

        sql_find = "SELECT * FROM FAVORITOS WHERE ID = :id"
        result = await execute_query_json(sql_find, {"id": id})

        if not result:
            raise HTTPException(status_code=404, detail="Favorito no encontrado")

        return result[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

