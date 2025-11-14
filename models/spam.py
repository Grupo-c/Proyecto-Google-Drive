from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
import re

class Spam(BaseModel):
    id_spam: int = Field(
        description = "ID de la carpeta spam"
    )
    
    id_usuario: int = Field(
        description = "ID del usuario perteneciente"
    )
    
    id_archivo: Optional[int] = Field(
        description = "ID del archivo en spam"
    )
    
    id_carpeta: Optional[int] = Field(
        description = "ID del archivo en carpeta"
    )
    
    fecha: datetime = Field(
        description = "Fecha en la que se coloco la carpeta/archivo en spam"
    )
