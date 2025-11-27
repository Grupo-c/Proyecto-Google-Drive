from pydantic import BaseModel, Field

class FoldersPermiso(BaseModel):
    id_usuario: int = Field(
        description = "ID del usuario que da el permiso"
    ) 
    
    id_folder: int = Field(
        description = "ID del folder que se da el permis"
    )
    
    id_permiso: int = Field(
        description = "ID del permiso otorgado"
    )
