from pydantic import BaseModel, Field
from typing import Optional

class ArchivosPermiso(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID del permiso de archivo"
    )
    
    id_archivo: int = Field(
        description = "ID del archivo que se da el permiso"
    )
    
    id_permiso: int = Field(
        description = "ID del permiso otorgado"
    )
