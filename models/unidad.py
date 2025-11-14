from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
import re

class Unidad(BaseModel):
    id: int = Field(
        description = "ID de la unidad asociada"
    )
    
    id_usuario: int = Field(
        description = "ID del usuario que le pertenece la unidad"
    )
    
    
    capacitad_total: float = Field(
        description = "Capacidad total de la unidad"
    )
    
    capacitad_actual: float = Field(
        description = "Capacidad actualmente usada en la carpeta"
    )
    
    id_membresia: int = Field(
        description = "ID de la membresia que tiene la unidad"
    )
    
    fecha_compra: date = Field(
        description = "Fecha en la que se compro la membresia null si no se compro ninguna"
    )
    
    fecha_expiracion: date = Field(
        description = "Fecha de expiracion de la membresia"
    )