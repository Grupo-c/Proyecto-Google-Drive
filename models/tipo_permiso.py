from pydantic import BaseModel, Field
from typing import Optional

class Permiso(BaseModel):
    id_permiso: int = Field(
        description="ID del permiso"
    )

    nombre: str = Field(
        description="Nombre del permiso", 
        examples=["Lectura", "Escritura"]
    )
    
    descripcion: Optional[str] = Field(
        default=None, 
        description="Descripción del permiso"
    )
