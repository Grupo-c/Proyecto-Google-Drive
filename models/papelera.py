from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
import re

class Papelera(BaseModel):
    id: Optional[int] = Field(
        description = "ID de la papelera"
    )

    id_usuario: int = Field(
        description = "ID del usuario" 
    )
    
    id_carpeta: Optional[int] = Field(
        description = "ID de la carpeta en la papelera"
    )
    
    id_archivo: Optional[str] = Field(
        description = "ID del archivo en la papelera"
    )
    
    tamaño: float = Field(
        description = "Tamaño usado en la carpeta"
    )
    
    fecha_entrada: date = Field(
        description = "Fecha en la que se metio el archivo en la papelera"
    )
    
    fecha_eliminacion: date = Field(
        description = "Fecha en la que se eliminara permanentemente los archivos/carpetas"
    )
    