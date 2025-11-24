from fastapi import FastAPI
import uvicorn
import os
import oracledb
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

from routes.usuario import router as usuario_router
from routes.archivo import router as archivo_router
from routes.carpeta import router as carpeta_router
from routes.unidad import router as unidad_router
from routes.favoritos import router as favoritos_router
from routes.comentarios import router as comentarios_router
from routes.compartidos import router as compartidos_router
from routes.descargas import router as descargas_router
from routes.icono import router as icono_router

app.include_router(usuario_router)
app.include_router(archivo_router)
app.include_router(carpeta_router)
app.include_router(unidad_router)
app.include_router(favoritos_router)
app.include_router(comentarios_router)
app.include_router(compartidos_router)
app.include_router(descargas_router)
app.include_router(icono_router)

SQL_USERNAME = os.getenv("SQL_USERNAME")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")
ORACLE_WALLET_PATH = os.getenv("ORACLE_WALLET_PATH")
ORACLE_DSN = os.getenv("ORACLE_DSN")
ORACLE_ENCODING = os.getenv("ORACLE_ENCODING", "UTF-8")
ORACLE_CLIENT_PATH = os.getenv("ORACLE_CLIENT_PATH")


oracledb.init_oracle_client(lib_dir=os.path.abspath(ORACLE_CLIENT_PATH))
os.environ["TNS_ADMIN"] = os.path.abspath(ORACLE_WALLET_PATH)

def test_oracle_connection():
    try:
        conn = oracledb.connect(
            user=SQL_USERNAME,
            password=SQL_PASSWORD,
            dsn=ORACLE_DSN
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM DUAL")
        cursor.fetchone()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error de conexión Oracle: {e}")
        return False


@app.get("/ready")
def readiness_check():
    db_status = test_oracle_connection()
    return {
        "status": "ready" if db_status else "not_ready",
        "database": "connected" if db_status else "disconnected",
        "service": "google-drive"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": "2025-11-22",
        "service": "google-drive",
        "environment": "production"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
