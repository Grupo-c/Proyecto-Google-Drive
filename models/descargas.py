from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Descarga(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID de la descarga"
    )
    id_usuario: int = Field(
        description="Usuario que realiza la descarga"
    )
    id_archivo: int = Field(
        description="Archivo descargado"
    )
    id_carpeta: Optional[int] = Field(
        default=None,
        description="Carpeta asociada a la descarga"
    )
    destino_descarga: str = Field(
        description="Ruta o destino de la descarga"
    )
    fecha_descarga: Optional[datetime] = Field(
        default=None,
        description="Fecha en que se realizó la descarga"
    )
    fecha_actualizacion: Optional[datetime] = Field(
        default=None,
        description="Fecha de última actualización de la descarga"
    )

class DescargaUpdate(BaseModel):
    destino_descarga: Optional[str] = Field(
        default=None,
        description="Ruta o destino de la descarga"
    )
    fecha_actualizacion: Optional[datetime] = Field(
        default=None,
        description="Fecha de última actualización de la descarga"
    )
