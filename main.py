from fastapi import FastAPI
import uvicorn

app = FastAPI()

from routes.usuario import router as usuario_router
from routes.archivo import router as archivo_router
from routes.carpeta import router as carpeta_router
from routes.unidad import router as unidad_router

app.include_router(usuario_router)
app.include_router(archivo_router)
app.include_router(carpeta_router)
app.include_router(unidad_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
