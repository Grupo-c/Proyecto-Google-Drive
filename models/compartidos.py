from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
import re

class Compartido(BaseModel):
    id: Optional[int] = Field(
        default=None, description="ID del registro de compartido"
    )

    id_usuario_receptor: int = Field(
        description = "Id del usuario que recibe el archivo/carpeta"
    )

    id_carpeta_compartida: Optional[int] = Field(
        description = "ID de la carpeta compartida"
    )

    id_archivo_compartido: Optional[int] = Field(
        description = "ID del archivo compartido"
    )

    id_tipo_permiso: int = Field(
        description = "ID de tipo de permiso"
    )

    
