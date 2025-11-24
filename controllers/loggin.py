import json
import logging
from fastapi import HTTPException

from utils.database import execute_query_json
from models.loggin import Login
from models.usuario import User
from utils.security import create_jwt_token

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =========================================================
#  REGISTRAR USUARIO (SIN FIREBASE) — SOLO ORACLE
# =========================================================
async def register_user(user: Login):

    query = """
        INSERT INTO GD.USUARIOS (correo, nombre, apellido, id_pais)
        VALUES (:correo, :nombre, :apellido, :id_pais)
        RETURNING id_usuario, correo, nombre, apellido, id_pais
            INTO :id_out, :correo_out, :nombre_out, :apellido_out, :pais_out
    """

    params = {
        "correo": user.correo,
        "nombre": user.nombre,
        "apellido": user.apellido,
        "id_pais": user.id_pais,
    }

    returning_vars = {
        "id_out": int,
        "correo_out": str,
        "nombre_out": str,
        "apellido_out": str,
        "pais_out": int,
    }

    try:
        result_json = await execute_query_json(
            query,
            params=params,
            needs_commit=True,
            returning_vars=returning_vars
        )

        return json.loads(result_json)

    except Exception as e:
        logger.error(f"Error al registrar usuario en Oracle: {e}")
        raise HTTPException(status_code=400, detail=f"Error al registrar usuario: {e}")


# =========================================================
#  LOGIN (SIN FIREBASE) — SOLO ORACLE + JWT LOCAL
# =========================================================
async def login_user(user: Login):
    query = """
        SELECT 
            id_usuario,
            nombre,
            apellido,
            correo,
            id_pais
        FROM GD.USUARIOS
        WHERE correo = :correo
          AND password = :password
    """

    params = {
        "correo": user.correo,
        "password": user.password
    }

    try:
        result_json = await execute_query_json(query, params)
        usuarios = json.loads(result_json)

        if not usuarios:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        u = usuarios[0]

        token = create_jwt_token(
            u["nombre"],
            u["apellido"],
            u["correo"]
        )

        return {
            "message": "Usuario autenticado exitosamente",
            "token": token,
            "usuario": u
        }

    except Exception as e:
        logger.exception("Error autenticando usuario en Oracle")
        raise HTTPException(status_code=500, detail="Error al autenticar usuario")


# =========================================================
#  OBTENER USUARIO POR CORREO (SIN FIREBASE)
# =========================================================
def get_usuario_por_correo(correo: str) -> User | None:

    query = """
        SELECT 
            id_usuario,
            nombre,
            apellido,
            correo,
            id_pais
        FROM GD.USUARIOS
        WHERE correo = :correo
    """

    try:
        result_json = execute_query_json(query, params={"correo": correo})
        usuarios = json.loads(result_json)

        if usuarios:
            u = usuarios[0]
            return User(
                id=u["id_usuario"],
                nombre=u["nombre"],
                apellido=u["apellido"],
                correo=u["correo"],
                id_pais=u["id_pais"]
            )

        return None

    except Exception as e:
        logger.error(f"Error obteniendo usuario: {e}")
        return None
