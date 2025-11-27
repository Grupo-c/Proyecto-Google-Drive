from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Papelera(BaseModel):
    id_papelera: int = Field(..., alias="ID_PAPELERA", description="ID de la entrada en la papelera")

    nombre_usuario: Optional[str] = Field(None, alias="NOMBRE_USUARIO", description="Nombre del usuario propietario")

    nombre_carpeta: Optional[str] = Field(None, alias="NOMBRE_CARPETA", description="Nombre de la carpeta si aplica")

    nombre_archivo: Optional[str] = Field(None, alias="NOMBRE_ARCHIVO", description="Nombre del archivo si aplica")

    tipo_archivo: Optional[str] = Field(None, alias="TIPO_ARCHIVO", description="Tipo/extension del archivo")

    tamano_archivo: Optional[str] = Field(None, alias="TAMANO_ARCHIVO", description="Tamaño legible del archivo (ej: '500 MB')")

    url_archivo: Optional[str] = Field(None, alias="URL_ARCHIVO", description="URL o ruta del archivo")

    fecha_agregado: Optional[datetime] = Field(None, alias="FECHA_AGREGADO", description="Fecha en que se movió a la papelera")

    fecha_eliminacion: Optional[datetime] = Field(None, alias="FECHA_ELIMINACION", description="Fecha prevista de eliminación permanente")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
        description = "Fecha en la que se metio el archivo en la papelera"
