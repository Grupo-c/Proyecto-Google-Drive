from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
import re

class Version(BaseModel):
    id: int = Field(
        description = "ID de la version"
    )

    id_archivo: int = Field(
        description = "ID del archivo que se versiona"
    )
    
    numero_version: int = Field(
        description = "Numero de la version que se le da el usuario"
    )
    
    fecha: date = Field(
        description = "Fecha en la que se actualizo o se puso la version"
    )
    
    id_autor: str = Field(
        description = "ID del autor de la version"
    )
    
    url: str = Field(
        description = "URL de la version"
    )