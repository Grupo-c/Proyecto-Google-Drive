from fastapi import APIRouter, status
from typing import List

from models.papelera import Papelera
from controllers.papelera import (
    get_trash_by_user,
    move_file_to_trash,
    move_folder_to_trash,
    restore_from_trash,
    delete_permanent,
    empty_trash,
)

router = APIRouter(prefix="/papelera")


@router.get("/usuario/{id_usuario}", tags=["Papelera"], status_code=status.HTTP_200_OK, response_model=List[Papelera])
async def get_papelera_usuario(id_usuario: int):
    result = await get_trash_by_user(id_usuario)
    return result


@router.post("/archivo/{id_archivo}/usuario/{id_usuario}", tags=["Papelera"], status_code=status.HTTP_201_CREATED, response_model=Papelera)
async def mover_archivo_a_papelera(id_archivo: int, id_usuario: int):
    result = await move_file_to_trash(id_archivo, id_usuario)
    return result


@router.post("/carpeta/{id_carpeta}/usuario/{id_usuario}", tags=["Papelera"], status_code=status.HTTP_201_CREATED, response_model=Papelera)
async def mover_carpeta_a_papelera(id_carpeta: int, id_usuario: int):
    result = await move_folder_to_trash(id_carpeta, id_usuario)
    return result


@router.delete("/restore/{id_papelera}", tags=["Papelera"], status_code=status.HTTP_200_OK)
async def restaurar_elemento(id_papelera: int):
    result = await restore_from_trash(id_papelera)
    return {"message": result}


@router.delete("/{id_papelera}", tags=["Papelera"], status_code=status.HTTP_200_OK)
async def eliminar_permanente(id_papelera: int):
    result = await delete_permanent(id_papelera)
    return {"message": result}


@router.delete("/usuario/{id_usuario}", tags=["Papelera"], status_code=status.HTTP_200_OK)
async def vaciar_papelera_usuario(id_usuario: int):
    result = await empty_trash(id_usuario)
    return {"message": result}