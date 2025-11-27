from fastapi import HTTPException
from models.compartidos import Compartido, CompartidoUpdate
from utils.database import execute_query_json

async def get_one_compartido(id: int) -> Compartido:
    sql = "SELECT * FROM COMPARTIDOS WHERE ID = :id"
    try:
        result = await execute_query_json(sql, {"id": id})
        if not result:
            raise HTTPException(status_code=404, detail="Compartido no encontrado")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_all_compartidos() -> list[Compartido]:
    sql = "SELECT * FROM COMPARTIDOS"
    try:
        return await execute_query_json(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def create_compartido(compartido: Compartido) -> Compartido:
    sql = """INSERT INTO COMPARTIDOS (ID_USUARIO, ID_ARCHIVO, ID_CARPETA, ID_PERMISO) 
             VALUES (:id_usuario, :id_archivo, :id_carpeta, :id_permiso)"""
    params = {
        "id_usuario": compartido.id_usuario,
        "id_archivo": compartido.id_archivo,
        "id_carpeta": compartido.id_carpeta,
        "id_permiso": compartido.id_permiso
    }
    try:
        await execute_query_json(sql, params, needs_commit=True)
        result = await execute_query_json(
            "SELECT * FROM COMPARTIDOS WHERE ID_USUARIO=:id_usuario AND ID_ARCHIVO=:id_archivo ORDER BY ID DESC",
            params
        )
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_compartido(id: int, compartido_update: CompartidosUpdate) -> Compartido:
    data = compartido_update.model_dump(exclude_none=True)
    if not data:
        raise HTTPException(status_code=400, detail="No se proporcionaron campos para actualizar")

    set_clause = ", ".join([f"{k} = :{k}" for k in data.keys()])
    sql = f"UPDATE COMPARTIDOS SET {set_clause} WHERE ID = :id"
    params = {**data, "id": id}
    try:
        await execute_query_json(sql, params, needs_commit=True)
        result = await execute_query_json("SELECT * FROM COMPARTIDOS WHERE ID = :id", {"id": id})
        return result[0] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def delete_compartido(id: int) -> str:
    sql = "DELETE FROM COMPARTIDOS WHERE ID = :id"
    try:
        await execute_query_json(sql, {"id": id}, needs_commit=True)
        return f"Compartido con id {id} eliminado correctamente."
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
