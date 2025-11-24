from dotenv import load_dotenv
import os
import oracledb
import logging
import asyncio

# Cargar variables de entorno
load_dotenv()

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración Oracle
USER = os.getenv("SQL_USERNAME")
PASSWORD = os.getenv("SQL_PASSWORD")
DSN = os.getenv("ORACLE_DSN")
CLIENT_PATH = os.getenv("ORACLE_CLIENT_PATH")

# Inicializar cliente Oracle (THICK MODE)
if CLIENT_PATH:
    oracledb.init_oracle_client(lib_dir=CLIENT_PATH)



def execute_query_sync(sql, params=None, needs_commit=False):
    conn = None
    cursor = None
    try:
        logger.info(f"Ejecutando SQL (sync): {sql}")

        conn = oracledb.connect(user=USER, password=PASSWORD, dsn=DSN)
        cursor = conn.cursor()

        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        results = []

        if cursor.description:  # SELECT
            columns = [col[0] for col in cursor.description]
            for row in cursor.fetchall():
                row = list(row)
                results.append(dict(zip(columns, row)))

        if needs_commit:
            conn.commit()

        return results

    except Exception as e:
        if conn and needs_commit:
            conn.rollback()
        raise Exception(f"Error ejecutando consulta: {str(e)}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



async def execute_query_json(sql, params=None, needs_commit=False):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        lambda: execute_query_sync(sql, params, needs_commit)
    )
