from pydantic import BaseModel, Field

class ArchivosPermiso(BaseModel):
    id_usuario: int = Field(
        description = "ID del usuario que da el permiso"
    )
    
    id_archivo: int = Field(
        description = "ID del archivo que se da el permiso"
    )
    
    id_permiso: int = Field(
        description = "ID del permiso otorgado"
    )
