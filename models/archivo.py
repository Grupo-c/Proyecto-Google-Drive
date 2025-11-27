from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
import re


class Archivo(BaseModel):
    id: Optional[int] = Field(
        default=None, 
        description="ID del archivo"
    )
    
    id_usuario: int = Field(
        description="Usuario propietario del archivo"
    )

    id_icono: int = Field(
    default=None,
    description="Icono asociado al archivo"
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

    fecha_creacion: Optional[datetime] = Field(
         default=None,
        description="Fecha de creación"
    )

    fecha_modificacion: Optional[datetime] = Field(
        default=None,
        description="Fecha de modificación"
    )

    url: str = Field(
        description="Ruta o URL donde se almacena el archivo"
    )

    visibilidad: Optional[bool] = Field(
        default=True, 
        description="Archivo público o privado"
    )

class ArchivoUpdate(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID del archivo a actualizar"
    )

    id_carpeta: Optional[int] = Field(
        default=None,
        description="Carpeta donde se almacena el archivo"
    )

    nombre: Optional[str] = Field(
        default=None,
        description="Nombre del archivo"
    )

    tamaño: Optional[float] = Field(
        default=None,
        description="Tamaño del archivo en MB"
    )
