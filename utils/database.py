from dotenv import load_dotenv
import os
import oracledb
import logging
import asyncio

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración de conexión desde .env
user = os.getenv("SQL_USERNAME")       # admin
password = os.getenv("SQL_PASSWORD")  # Proyecto-bases123
dsn = os.getenv("ORACLE_DSN")         # googledrive_high
client_path = os.getenv("ORACLE_CLIENT_PATH")  # C:\oracle\instantclient_23_0

# Inicializar cliente Oracle (Thick)
if client_path:
    oracledb.init_oracle_client(lib_dir=client_path)

async def get_db_connection():
    """
    Obtiene una conexión a la base de datos Oracle usando oracledb (Thick).
    """
    try:
        logger.info("Intentando conectar a Oracle DB...")
        # Conexión sin 'encoding' explícito
        conn = oracledb.connect(user=user, password=password, dsn=dsn)
        logger.info("Conexión exitosa a Oracle DB.")
        return conn
    except oracledb.Error as e:
        logger.error(f"Error de conexión a Oracle: {str(e)}")
        raise Exception(f"Error de conexión a Oracle: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado durante la conexión: {str(e)}")
        raise

async def execute_query_json(sql_template, params=None, needs_commit=False):
    conn = None
    cursor = None
    try:
        conn = await get_db_connection()
        cursor = conn.cursor()
        param_info = "(sin parámetros)" if not params else f"(con {len(params)} parámetros)"
        logger.info(f"Ejecutando consulta {param_info}: {sql_template}")

        if params:
            cursor.execute(sql_template, params)
        else:
            cursor.execute(sql_template)

        results = []
        if cursor.description:
            columns = [col[0] for col in cursor.description]
            for row in cursor.fetchall():
                processed_row = [str(item) if isinstance(item, (bytes, bytearray)) else item for item in row]
                results.append(dict(zip(columns, processed_row)))

        if needs_commit:
            conn.commit()

        return results

    except oracledb.Error as e:
        if conn and needs_commit:
            conn.rollback()
        raise Exception(f"Error ejecutando consulta: {str(e)}") from e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
