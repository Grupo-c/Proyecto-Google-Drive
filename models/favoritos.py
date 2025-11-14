from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
import re

class Favorito(BaseModel):
    id_favorito: int = Field(
        description = "ID del favorito"
    )

    id_usuario: int = Field(
        description = "ID del usuario"
    )

    id_archivo: Optional[int] = Field(
        description = "ID del archivo en la carpeta favorito"
    )

    id_carpeta: Optional[int] = Field(
        description = "ID de la carpeta favorita"
    )

    fecha: datetime = Field(
        description = "Fecha en la que se puso la carpeta/archivo en favoritos"
    )