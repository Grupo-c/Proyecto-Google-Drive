import os
import json
import logging
import firebase_admin
import requests
from pathlib import Path
from fastapi import HTTPException
from firebase_admin import credentials, auth as firebase_auth
from dotenv import load_dotenv

from utils.database import execute_query_json
from models.loggin import Login
from models.usuario import User
from utils.security import create_jwt_token
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Detectar ruta del proyecto y del JSON de Firebase
BASE_DIR = Path(__file__).resolve().parent.parent
SERVICE_ACCOUNT_PATH = BASE_DIR / "secrets" / "credenciales.json"
print(f"Usando service account: {SERVICE_ACCOUNT_PATH}")

# Inicializar Firebase solo si no está inicializado
if not firebase_admin._apps:
    cred = credentials.Certificate(str(SERVICE_ACCOUNT_PATH))
    firebase_admin.initialize_app(cred)

async def register_user_firebase(user: Login):
    try:
        user_record = firebase_auth.create_user(
            email=user.correo,
            password=user.password
        )
        logger.info(f"Usuario creado en Firebase con UID: {user_record.uid}")
        
    except firebase_admin.exceptions.FirebaseError as e:
        logger.error(f"Error al registrar usuario en Firebase: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Error al registrar usuario: {str(e)}")
    
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
        "id_pais": user.id_pais
    }
    
    returning_vars = {
        "id_out": int,
        "correo_out": str,
        "nombre_out": str,
        "apellido_out": str,
        "pais_out": int
    }
    try:
        result_json = execute_query_json(
            query,
            params=params,
            needs_commit=True,
            returning_vars=returning_vars
        )
        return json.loads(result_json)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al registrar usuario: {e}")
   
    
    


async def login_user_firebase(user: Login):
    api_key = os.getenv("FIREBASE_API_KEY")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

    payload = {"email": user.correo, "password": user.contraseña, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    response_data = response.json()

    if "error" in response_data:
        logger.warning(f"Firebase login failed: {response_data['error']}")
        raise HTTPException(
            status_code=400,
            detail=f"Error al autenticar usuario: {response_data['error']['message']}"
        )

    query = """
        SELECT correo, nombre, apellido
        FROM GD.USUARIOS
        WHERE correo = :correo

    """

    try:
        result_json =  execute_query_json(query, (user.correo,), needs_commit=False)
        result_dict = json.loads(result_json)

        if not result_dict:
            raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")

        user_db = result_dict[0]

        return {
            "message": "Usuario autenticado exitosamente",
            "idToken": create_jwt_token(
                user_db["nombre"],
                user_db["apellido"],
                user.correo,
            )
        }
    except Exception as e:
        logger.exception("Error obteniendo datos del usuario en Oracle")
        raise HTTPException(status_code=500, detail="Error obteniendo datos del usuario")

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
    result = execute_query_json(query, params={"correo": correo})
    usuarios = json.loads(result)
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