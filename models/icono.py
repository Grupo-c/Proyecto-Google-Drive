from pydantic import BaseModel, Field
from typing import Optional

class Icono(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID del icono"
    )
    nombre: str = Field(
        description="Nombre del icono"
    )
    url: str = Field(
        description="URL del icono"
    )

class IconoUpdate(BaseModel):
    nombre: Optional[str] = Field(
        default=None,
        description="Nombre del icono"
    )
    url: Optional[str] = Field(
        default=None,
        description="URL del icono"
    )