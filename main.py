from fastapi import FastAPI
from utils.database import execute_query_json
import uvicorn

app = FastAPI()

@app.get("/usuarios")
async def get_usuarios():
    query = """
        SELECT 
            ID,
            NOMBRE,
            APELLIDO,
            CORREO,
            FOTO,
            ID_PAIS
        FROM GD.USUARIO;
    """
    result = await execute_query_json(query)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
