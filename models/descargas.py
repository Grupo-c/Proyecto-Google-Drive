from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
import re

class Descarga(BaseModel):

    id_carpeta_offline: Optional[int] = Field(
        description = "ID de la carpeta descargada"
    )
    
    id_archivo_offline: Optional[int] = Field(
        description = "ID del archivo descargado"
    )

    id_usuario: int = Field(
        description = "ID del usuario que descargo"
    )

    fecha_sincronizacion: datetime = Field(
        description = "Fecha de descarga inicial"
    )
    
    fecha_de_actualizacion: datetime = Field(
        description = "Fecha de actualizacion de la descarga"
    )
    
    local_path: str = Field(
        description = "Ruta de la descarga"
    )
