from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional

class Modelo(BaseModel):

    instructor: str
    email: EmailStr
    fichas: list
    argregarArchivo : Optional[bool] = False


