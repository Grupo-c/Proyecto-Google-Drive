from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Comentario(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID del comentario"
    )
    id_usuario: int = Field(
        description="ID del usuario que hace el comentario"
    )
    id_archivo: int = Field(
        description="ID del archivo al que se hace el comentario"
    )
    texto: str = Field(
        description="Texto del comentario"
    )
    fecha: Optional[datetime] = Field(
        default=None,
        description="Fecha de cuando se hizo el comentario"
    )
