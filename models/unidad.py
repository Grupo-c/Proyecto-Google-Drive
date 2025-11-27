from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Unidad(BaseModel):
    id: Optional[int] = Field(
        default=None, 
        description="ID de la unidad asociada (autogenerado)"
        )
    
    id_usuario: int = Field(
        description="ID del usuario que le pertenece la unidad"
        )
    
    capacidad_total: float = Field(
        description="Capacidad total de la unidad"
        )
    
    capacidad_actual: float = Field(
        description="Capacidad actualmente usada en la unidad"
        )

    id_membresia: int = Field(
        description="ID de la membresía que tiene la unidad"
        )

    fecha_compra: Optional[date] = Field(
        default=None, 
        description="Fecha de compra de la membresía"
        )

    fecha_expiracion: Optional[date] = Field(
        default=None, 
        description="Fecha de expiración de la membresía"
        )
