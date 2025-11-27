from pydantic import BaseModel, Field
from typing import Optional

class Membresia(BaseModel):
    id: Optional[int] = Field(
        default=None
        )
    
    nombre: str = Field(
        description="Nombre de la membresia"
    )
    
    precio: float = Field(
        description="Precio de la membresia"
    )
