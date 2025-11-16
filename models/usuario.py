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
    
    contraseña: str = Field(
        min_length=8,
        max_length=64,
        description="Contraseña del usuario, debe tener entre 8 y 64 caracteres incluir por lo menos un numero, por lo menos una mayuscula y por lo menos un caracter especial.",
        examples=["MiPassword123!"]
    )

    foto: Optional[str] = Field(
        default=None,
        description="URL"
    )
    @field_validator('contraseña')
    @classmethod
    def validate_password_complexity(cls, value: str):
        if not re.search(r"[A-Z]", value):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r"\d", value):
            raise ValueError("La contraseña debe contener al menos un número.")
        if not re.search(r"[@$!%*?&]", value):
            raise ValueError("La contraseña debe contener al menos un carácter especial (@$!%*?&).")
        return value
