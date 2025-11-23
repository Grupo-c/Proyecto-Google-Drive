from fastapi import APIRouter, status
from models.compartidos import Compartido
from controllers.compartidos import (
    get_shared_by_user,
    get_one_shared,
    create_shared,
    update_shared,
    delete_shared
)

router = APIRouter(prefix="/shared")

# Obtener todos los compartidos de un usuario
@router.get("/", tags=["Shared"], status_code=status.HTTP_200_OK)
async def get_all_shared_by_user(id_usuario: int):
    result = await get_shared_by_user(id_usuario)
    return result

# Crear un nuevo compartido
@router.post("/", tags=["Shared"], status_code=status.HTTP_201_CREATED)
async def create_new_shared(compartido_data: Compartido):
    result = await create_shared(compartido_data)
    return result

# Obtener un compartido por ID
@router.get("/{id}", tags=["Shared"], status_code=status.HTTP_200_OK)
async def get_shared_by_id(id: int):
    result = await get_one_shared(id)
    return result

# Actualizar un compartido por ID
@router.put("/{id}", tags=["Shared"], status_code=status.HTTP_200_OK)
async def update_shared_by_id(compartido_data: Compartido, id: int):
    compartido_data.id = id
    result = await update_shared(compartido_data)
    return result

# Eliminar un compartido por ID
@router.delete("/{id}", tags=["Shared"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_shared_by_id(id: int):
    await delete_shared(id)
    return None
