from fastapi import APIRouter, status
from models.descargas import Descarga, DescargaUpdate
from controllers.descargas import get_all_descargas, get_one_descarga, create_descarga, update_descarga, delete_descarga


router = APIRouter(prefix="/descargas")

@router.get("/", tags=["Descargas"], status_code=status.HTTP_200_OK)
async def get_all_descargas():
    return await get_all_descargas()

@router.get("/{id}", tags=["Descargas"], status_code=status.HTTP_200_OK)
async def get_one_descarga(id: int):
    return await get_one_descarga(id)

@router.post("/", tags=["Descargas"], status_code=status.HTTP_201_CREATED)
async def create_new_descarga(descarga_data: Descarga):
    return await create_descarga(descarga_data)

@router.put("/{id}", tags=["Descargas"], status_code=status.HTTP_200_OK)
async def update_descarga_info(id: int, descarga_data: DescargaUpdate):
    return await update_descarga(id, descarga_data)

@router.delete("/{id}", tags=["Descargas"], status_code=status.HTTP_200_OK)
async def delete_descarga(id: int):
    return {"message": await delete_descarga(id)}
