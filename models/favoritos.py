from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
import re

class Favorito(BaseModel):
    model_config = {
        "populate_by_name": True
    }
    id_favorito: Optional[int] = Field(
        default=None,
        alias="ID",
        description="ID del favorito"
    )
    id_usuario: Optional[int] = Field(
        alias="ID_USUARIO",
        description="ID del usuario"
    )
    id_archivo: Optional[int] = Field(
        alias="ID_ARCHIVO",
        description="ID del archivo en la carpeta favorito"
    )
    id_carpeta: Optional[int] = Field(
        alias="ID_CARPETA",
        description="ID de la carpeta favorita"
    )
    fecha_agregado: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        alias="FECHA_AGREGADO",
        description="Fecha en que se agregó el favorito"
    )

class FavoritoUpdate(BaseModel):
    id_usuario: Optional[int] = None
    id_archivo: Optional[int] = None
    id_carpeta: Optional[int] = None

    model_config = {
        "populate_by_name": True
    }
