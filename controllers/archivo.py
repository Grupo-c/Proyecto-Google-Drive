from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re

class Archivo(BaseModel):

    id: Optional[int] = Field(
        default=None,
        description="ID del archivo",
        gt=0,
        examples=[1001, 2022]
    )

    usuario_id: int = Field(
        description="ID del usuario propietario del archivo",
        gt=0,
        examples=[1, 45]
    )

    carpeta_id: Optional[int] = Field(
        default=None,
        description="ID de la carpeta",
        gt=0,
        examples=[10, 20]
    )

    iconos_id: int = Field(
        description="ID del icono asignado al archivo",
        gt=0,
        examples=[3, 7]
    )

    nombre: str = Field(
        description="Nombre del archivo",
        min_length=1,
        max_length=255,
        examples=["documento.pdf", "foto.png"]
    )

    tipo: str = Field(
        description="Tipo/Extensión del archivo",
        pattern=r"^[A-Za-z0-9_-]+\.[A-Za-z0-9]+$",
        examples=["documento.pdf", "imagen.jpeg"]
    )

    tamaño: float = Field(
        description="Tamaño del archivo en bytes",
        gt=0,
        examples=[1024.5, 500000.0]
    )

    fecha_creacion: Optional[datetime] = Field(
        default=None,
        description="Fecha en que se creó el archivo",
        examples=["2025-05-15T12:30:00"]
    )

    fecha_modificacion: Optional[datetime] = Field(
        default=None,
        description="Fecha de última modificación",
        examples=["2025-05-20T09:10:00"]
    )

    url: str = Field(
        description="URL donde se almacena el archivo",
        min_length=1,
        max_length=300,
        examples=["/uploads/archivo.pdf", "https://server.com/img.png"]
    )

    visibilidad: bool = Field(
        description="True = archivo público, False = archivo privado",
        examples=[True]
    )

    @field_validator('tipo')
    @classmethod
    def validate_file_type(cls, value: str):
        if not re.match(r"^[A-Za-z0-9_-]+\.[A-Za-z0-9]+$", value):
            raise ValueError("El tipo de archivo debe seguir el formato 'nombre.ext'.")
        return value