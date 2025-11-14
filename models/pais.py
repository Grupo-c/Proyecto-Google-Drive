from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
import re

class Pais(BaseModel):
    id: int = Field(
        description = "ID del pais"
    )
    
    nombre: str = Field(
        description="Nombre del país", 
        examples=["Honduras", "México"]
    )