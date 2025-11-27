from pydantic import BaseModel, Field
from typing import Optional

class Carpeta(BaseModel):
    id: Optional[int] = Field(
        default=None, 
        description="ID de la carpeta",
        exclude=True
        )
    
    id_usuario: int = Field(
        description="Usuario propietario de la carpeta"
        )
    
    id_carpeta_padre: Optional[int] = Field(
        default=None, 
        description="Carpeta padre, si existe"
        )
    
    nombre: Optional[str] = Field(
        description="Nombre de la carpeta"
        )

class CarpetaUpdate(BaseModel):
    id: Optional[int] = Field(
        default=None, 
        description="ID de la carpeta", 
        exclude=True
        )
    id_carpeta_padre: Optional[int] = Field(
        default=None, 
        description="ID de la carpeta padre"
        )
    nombre: Optional[str] = Field(
        default=None, 
        description="Nuevo nombre de la carpeta"
        )