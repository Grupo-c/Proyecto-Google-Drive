from fastapi import HTTPException
import logging
from typing import List

from models.papelera import Papelera
from utils.database import execute_query_json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_trash_by_user(id_usuario: int) -> List[Papelera]:
	sql = """
		SELECT P.*, A.NOMBRE AS NOMBRE_ARCHIVO, C.NOMBRE AS NOMBRE_CARPETA
		FROM PAPELERA P
		LEFT JOIN ARCHIVO A ON P.ID_ARCHIVO = A.ID
		LEFT JOIN CARPETA C ON P.ID_CARPETA = C.ID
		WHERE P.ID_USUARIO = :id_usuario
	"""
	try:
		return await execute_query_json(sql, {"id_usuario": id_usuario})
	except Exception as e:
		logger.error(f"Error al obtener papelera para usuario {id_usuario}: {e}")
		raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e

async def move_file_to_trash(id_archivo: int, id_usuario: int) -> Papelera:
	try:
		# Verificar si ya está en papelera
		exists_sql = "SELECT COUNT(*) AS CNT FROM PAPELERA WHERE ID_ARCHIVO = :id_archivo"
		exists = await execute_query_json(exists_sql, {"id_archivo": id_archivo})
		if exists and exists[0].get("CNT", 0) > 0:
			raise HTTPException(status_code=400, detail="Archivo ya está en la papelera")

		# Obtener tamaño del archivo
		sql_size = "SELECT TAMANO FROM ARCHIVO WHERE ID = :id_archivo"
		res = await execute_query_json(sql_size, {"id_archivo": id_archivo})
		if not res:
			raise HTTPException(status_code=404, detail="Archivo no encontrado")
		tamano = res[0].get("TAMANO", 0)

		# Insertar en papelera
		insert_sql = """
			INSERT INTO PAPELERA (ID_USUARIO, ID_ARCHIVO, TAMANO)
			VALUES (:id_usuario, :id_archivo, :tamano)
		"""
		await execute_query_json(insert_sql, {"id_usuario": id_usuario, "id_archivo": id_archivo, "tamano": tamano}, needs_commit=True)

		# Devolver el registro recién insertado
		find_sql = "SELECT * FROM PAPELERA WHERE ID_ARCHIVO = :id_archivo ORDER BY ID DESC"
		result = await execute_query_json(find_sql, {"id_archivo": id_archivo})
		return result[0] if result else None

	except HTTPException:
		raise
	except Exception as e:
		logger.error(f"Error al mover archivo {id_archivo} a papelera: {e}")
		raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e

async def move_folder_to_trash(id_carpeta: int, id_usuario: int) -> Papelera:
	try:
		exists_sql = "SELECT COUNT(*) AS CNT FROM PAPELERA WHERE ID_CARPETA = :id_carpeta"
		exists = await execute_query_json(exists_sql, {"id_carpeta": id_carpeta})
		if exists and exists[0].get("CNT", 0) > 0:
			raise HTTPException(status_code=400, detail="Carpeta ya está en la papelera")

		sql_size = "SELECT TAMANO FROM CARPETA WHERE ID = :id_carpeta"
		res = await execute_query_json(sql_size, {"id_carpeta": id_carpeta})
		if not res:
			raise HTTPException(status_code=404, detail="Carpeta no encontrada")
		tamano = res[0].get("TAMANO", 0)

		insert_sql = """
			INSERT INTO PAPELERA (ID_USUARIO, ID_CARPETA, TAMANO)
			VALUES (:id_usuario, :id_carpeta, :tamano)
		"""
		await execute_query_json(insert_sql, {"id_usuario": id_usuario, "id_carpeta": id_carpeta, "tamano": tamano}, needs_commit=True)

		find_sql = "SELECT * FROM PAPELERA WHERE ID_CARPETA = :id_carpeta ORDER BY ID DESC"
		result = await execute_query_json(find_sql, {"id_carpeta": id_carpeta})
		return result[0] if result else None

	except HTTPException:
		raise
	except Exception as e:
		logger.error(f"Error al mover carpeta {id_carpeta} a papelera: {e}")
		raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e

async def restore_from_trash(id_papelera: int) -> str:
	sql_check = "SELECT ID_ARCHIVO, ID_CARPETA FROM PAPELERA WHERE ID = :id"
	try:
		res = await execute_query_json(sql_check, {"id": id_papelera})
		if not res:
			raise HTTPException(status_code=404, detail="Entrada en papelera no encontrada")

		# Para restaurar sólo se elimina la referencia en PAPELERA.
		sql_delete = "DELETE FROM PAPELERA WHERE ID = :id"
		await execute_query_json(sql_delete, {"id": id_papelera}, needs_commit=True)
		return f"Elemento restaurado correctamente (id papelera {id_papelera})"
	except HTTPException:
		raise
	except Exception as e:
		logger.error(f"Error al restaurar elemento papelera {id_papelera}: {e}")
		raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e

async def delete_permanent(id_papelera: int) -> str:
	sql_find = "SELECT ID_ARCHIVO, ID_CARPETA FROM PAPELERA WHERE ID = :id"
	try:
		res = await execute_query_json(sql_find, {"id": id_papelera})
		if not res:
			raise HTTPException(status_code=404, detail="Entrada en papelera no encontrada")

		row = res[0]
		id_archivo = row.get("ID_ARCHIVO")
		id_carpeta = row.get("ID_CARPETA")

		if id_archivo:
			# Eliminar dependencias y luego el archivo
			sql_cleanup = """
			BEGIN
				DELETE FROM FAVORITOS WHERE ID_ARCHIVO = :id_archivo;
				DELETE FROM SPAM WHERE ID_ARCHIVO = :id_archivo;
				DELETE FROM COMPARTIDOS WHERE ID_ARCHIVO = :id_archivo;
				DELETE FROM VERSION WHERE ID_ARCHIVO = :id_archivo;
				DELETE FROM ARCHIVO WHERE ID = :id_archivo;
			END;
			"""
			await execute_query_json(sql_cleanup, {"id_archivo": id_archivo}, needs_commit=True)

		elif id_carpeta:
			# Eliminar archivos dentro de la carpeta y luego la carpeta
			sql_cleanup = """
			BEGIN
				FOR r IN (SELECT ID FROM ARCHIVO WHERE ID_CARPETA = :id_carpeta) LOOP
					DELETE FROM FAVORITOS WHERE ID_ARCHIVO = r.ID;
					DELETE FROM SPAM WHERE ID_ARCHIVO = r.ID;
					DELETE FROM COMPARTIDOS WHERE ID_ARCHIVO = r.ID;
					DELETE FROM VERSION WHERE ID_ARCHIVO = r.ID;
					DELETE FROM ARCHIVO WHERE ID = r.ID;
				END LOOP;
				DELETE FROM CARPETA WHERE ID = :id_carpeta;
			END;
			"""
			await execute_query_json(sql_cleanup, {"id_carpeta": id_carpeta}, needs_commit=True)

		# Finalmente eliminar la entrada en PAPELERA
		sql_delete = "DELETE FROM PAPELERA WHERE ID = :id"
		await execute_query_json(sql_delete, {"id": id_papelera}, needs_commit=True)

		return f"Elemento con id papelera {id_papelera} eliminado permanentemente."

	except HTTPException:
		raise
	except Exception as e:
		logger.error(f"Error al eliminar permanentemente entrada {id_papelera}: {e}")
		raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e

async def empty_trash(id_usuario: int) -> str:
	try:
		sql_list = "SELECT ID FROM PAPELERA WHERE ID_USUARIO = :id_usuario"
		items = await execute_query_json(sql_list, {"id_usuario": id_usuario})
		if not items:
			return "Papelera vacía"

		# Borrar permanentemente cada elemento
		for it in items:
			pid = it.get("ID")
			await delete_permanent(pid)

		return "Papelera vaciada correctamente"
	except Exception as e:
		logger.error(f"Error al vaciar papelera para usuario {id_usuario}: {e}")
		raise HTTPException(status_code=500, detail=f"Database error: {str(e)}") from e


