from fastapi import HTTPException
from models.descargas import Descarga, DescargaUpdate
from utils.database import execute_query_json

async def get_one_descarga(id: int) -> Descarga:
    sql = "SELECT * FROM DESCARGAS WHERE ID = :id"
    try:
        result = await execute_query_json(sql, {"id": id})
        if not result:
            raise HTTPException(status_code=404, detail="Descarga no encontrada")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_all_descargas() -> list[Descarga]:
    sql = "SELECT * FROM DESCARGAS"
    try:
        return await execute_query_json(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def create_descarga(descarga: Descarga) -> Descarga:
    sql = """INSERT INTO DESCARGAS (ID_USUARIO, ID_ARCHIVO, ID_CARPETA, DESTINO_DESCARGA) 
             VALUES (:id_usuario, :id_archivo, :id_carpeta, :destino_descarga)"""
    params = {
        "id_usuario": descarga.id_usuario,
        "id_archivo": descarga.id_archivo,
        "id_carpeta": descarga.id_carpeta,
        "destino_descarga": descarga.destino_descarga
    }
    try:
        await execute_query_json(sql, params, needs_commit=True)
        result = await execute_query_json(
            "SELECT * FROM DESCARGAS WHERE ID_USUARIO=:id_usuario AND ID_ARCHIVO=:id_archivo ORDER BY ID DESC",
            params
        )
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_descarga(id: int, descarga_update: DescargaUpdate) -> Descarga:
    data = descarga_update.model_dump(exclude_none=True)
    if not data:
        raise HTTPException(status_code=400, detail="No se proporcionaron campos para actualizar")

    set_clause = ", ".join([f"{k} = :{k}" for k in data.keys()])
    sql = f"UPDATE DESCARGAS SET {set_clause} WHERE ID = :id"
    params = {**data, "id": id}
    try:
        await execute_query_json(sql, params, needs_commit=True)
        result = await execute_query_json("SELECT * FROM DESCARGAS WHERE ID = :id", {"id": id})
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def delete_descarga(id: int) -> str:
    sql = "DELETE FROM DESCARGAS WHERE ID = :id"
    try:
        await execute_query_json(sql, {"id": id}, needs_commit=True)
        return f"Descarga con id {id} eliminada correctamente."
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
