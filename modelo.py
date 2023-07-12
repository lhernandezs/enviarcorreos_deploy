from pydantic import BaseModel
from pydantic import EmailStr

class Modelo(BaseModel):

    instructor: str
    email: EmailStr
    fichas: list


