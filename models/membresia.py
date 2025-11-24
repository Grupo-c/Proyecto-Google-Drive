
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Membresia(BaseModel):
    id_membresia: int = Field(
        alias = "ID",
        description = "ID de la membresia"
    )

    nombre: str = Field(
        alias= "NOMBRE",
        description = "Nombre de la membresia"
    )

    precio: float = Field(
        alias= "PRECIO",
        description = "Precio de la membresia"
    )
