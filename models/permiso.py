from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
import re

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


class ArchivosPermiso(BaseModel):
    id_usuario: int = Field(
        description = "ID del usuario que da el permiso"
    )
    
    id_archivo: int = Field(
        description = "ID del archivo que se da el permiso"
    )
    
    id_permiso: int = Field(
        description = "ID del permiso otorgado"
    )


class FoldersPermiso(BaseModel):
    id_usuario: int = Field(
        description = "ID del usuario que da el permiso"
    ) 
    
    id_folder: int = Field(
        description = "ID del folder que se da el permis"
    )
    
    id_permiso: int = Field(
        description = "ID del permiso otorgado"
    )