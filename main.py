from fastapi import FastAPI
import uvicorn

app = FastAPI()

from routes.usuario import router as usuario_router
from routes.archivo import router as archivo_router
app.include_router(usuario_router)
app.include_router(archivo_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
