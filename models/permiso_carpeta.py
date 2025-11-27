from pydantic import BaseModel, Field
from typing import Optional

class FoldersPermiso(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="ID del folder_permiso"
    ) 
    id_carpeta: int = Field(
        description="ID del folder al que se da el permiso"
    )
    id_permiso: int = Field(
        description="ID del permiso otorgado"
    )
