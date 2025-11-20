from fastapi import FastAPI
import uvicorn
import pyodbc
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

app = FastAPI()

from routes.usuario import router as usuario_router
from routes.archivo import router as archivo_router
from routes.carpeta import router as carpeta_router
from routes.unidad import router as unidad_router
from routes.favoritos import router as favoritos_router


app.include_router(usuario_router)
app.include_router(archivo_router)
app.include_router(carpeta_router)
app.include_router(unidad_router)
app.include_router(favoritos_router)


# Leer credenciales desde .env
DB_DRIVER = os.getenv("DB_DRIVER")
SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USERNAME = os.getenv("SQL_USERNAME")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

def test_sql_connection():
    try:
        conn_str = (
            f"DRIVER={DB_DRIVER};"
            f"SERVER={SQL_SERVER};"
            f"DATABASE={SQL_DATABASE};"
            f"UID={SQL_USERNAME};"
            f"PWD={SQL_PASSWORD}"
        )
        with pyodbc.connect(conn_str, timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return True
    except Exception as e:
        print(f"Error de conexión SQL: {e}")
        return False

@app.get("/ready")
def readiness_check():
    db_status = test_sql_connection()
    return {
        "status": "ready" if db_status else "not_ready",
        "database": "connected" if db_status else "disconnected",
        "service": "google-drive"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": "2025-08-02",
        "service": "google-drive",
        "environment": "production"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
