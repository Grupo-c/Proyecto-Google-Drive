from pydantic import BaseModel, Field
from typing import Optional

class Pais(BaseModel):
    id: Optional[int] = Field(
        default=None
    )
    nombre: str = Field(
        description="Nombre del pais"
    )
