
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
import re

class Comentario(BaseModel):
    id: Optional[int] = Field(
        description = "ID del comentario"
    )

    id_usuario_comentador: int = Field(
        description = "ID del usuario que hace el comentario"
    )

    id_archivo: int = Field(
        description = "ID del archivo al que se hace el comentario"
    )

    texto: str = Field(
        description="Texto del comentario"
    )

    fecha: date = Field(
        description = "Fecha de cuando se hizo el comentario"
    )