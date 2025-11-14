from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
import re


class Archivo(BaseModel):
    id: Optional[int] = Field(
        default=None, 
        description="ID del archivo"
    )
    
    id_propietario: int = Field(
        description="Usuario propietario del archivo"
    )

    id_carpeta: Optional[int] = Field(
        description="Carpeta donde se almacena el archivo"
    )

    nombre: str = Field(
        description="Nombre del archivo", 
        examples=["informe.pdf"]
    )

    tipo: str = Field(
        description="Tipo MIME o extensión", 
        examples=["PDF", "DOCX"]
    )

    tamaño: float = Field(
        description="Tamaño del archivo en MB", 
        examples=[5.2]
    )

    fecha_creacion: date = Field(
        description="Fecha de creación"
    )

    fecha_modificacion: date = Field(
        description="Fecha de modificación"
    )

    url: str = Field(
        description="Ruta o URL donde se almacena el archivo"
    )

    visibilidad: Optional[bool] = Field(
        default=True, 
        description="Archivo público o privado"
    )