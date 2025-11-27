from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class User(BaseModel):
    id: Optional[int] = Field(default=None, alias="ID")
    nombre: str = Field(
        alias="NOMBRE",
        description="User First Name",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Juan", "María José"]
    )
    apellido: str = Field(
        alias="APELLIDO",
        description="User Last Name",
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' -]+$",
        examples=["Pérez", "García López"]
    )
    correo: str = Field(
        alias="CORREO",
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        examples=["usuario@example.com"]
    )
    id_pais: int = Field(
        alias="ID_PAIS", 
        description="ID del país del usuario")
    foto: Optional[str] = Field(
        default=None, alias="FOTO", 
        description="URL")