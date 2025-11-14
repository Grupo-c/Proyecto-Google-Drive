from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime

class Carpeta(BaseModel):
    id: Optional[int] = Field(
        default=None, 
        description="ID de la carpeta"
    )

    id_usuario: int = Field(
        description="Usuario propietario de la carpeta"
    )

    id_carpeta_padre: Optional[int] = Field(
        default=None, description="Carpeta padre, si existe"
    )

    nombre: str = Field(
        description="Nombre de la carpeta", 
        examples=["Documentos", "Fotos"]
    )
    
    tamaño: float = Field(
        description="Tamaño de la carpeta en MB", 
        examples=[12.5]
    )

    fecha_creacion: date = Field(
        description="Fecha de creación de la carpeta"
    )

    fecha_modificacion: date = Field(
        description="Fecha de última modificación"
    )

    visibilidad: Optional[bool] = Field(
        default=True, description="Visibilidad pública o privada"
    )
