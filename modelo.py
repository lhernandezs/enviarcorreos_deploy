from pydantic import BaseModel, EmailStr
from typing import Optional

class Modelo(BaseModel):

    instructor: str
    email: EmailStr
    fichas: list
    agregarArchivo : Optional[bool] = False

class Salida(BaseModel):
    reporte: list