from datetime import date
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
#from typing import List

class Modelo(BaseModel):

    instructor: str
    email: EmailStr
    fichas: list
    show_information: bool = False

