from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class User(BaseModel):
    id: Optional[int] = Field(
        default=None,
    )

    nombre: str = Field(
        description="User First Name",
        pattern= r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Juan", "María José"]
    )

    apellido: str = Field(
        description="User Last Name",
        pattern= r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Pérez", "García López"]
    )

    correo: str = Field(
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        examples=["usuario@example.com"]
    )   

    id_pais: int = Field(
        description="ID del país del usuario"
    )

    foto: Optional[str] = Field(
        default=None,
        description="URL"
    )