from pydantic import BaseModel, Field
from typing import Optional

class Compartido(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID del registro de compartido"
    )
    id_usuario: int = Field(
        description="Usuario que comparte"
    )
    id_archivo: int = Field(
        description="Archivo compartido"
    )
    id_carpeta: Optional[int] = Field(
        default=None,
        description="Carpeta compartida"
    )
    id_permiso: int = Field(
        description="Permiso asignado"
    )

class CompartidoUpdate(BaseModel):
    id_carpeta: Optional[int] = Field(
        default=None,
        description="Carpeta compartida"
    )
    id_permiso: Optional[int] = Field(
        default=None,
        description="Permiso asignado"
    )
    
