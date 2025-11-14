
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Membresia(BaseModel):
    id_membresia: int = Field(
        description = "ID de la membresia"
    )

    nombre: str = Field(
        description = "Nombre de la membresia"
    )

    precio: float = Field(
        description = "Precio de la membresia"
    )

    descripcion: Optional[str] = Field(
        description = "Descripcion de la membresia"
    )