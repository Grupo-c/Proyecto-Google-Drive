
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
import re

class Icono(BaseModel):
    id_icono: int = Field(
        description = "ID del icono"
    )

    nombre: str = Field(
        description = "Nombre del icono"
    )

    url: str = Field(
        description = "URL del icono"
    )