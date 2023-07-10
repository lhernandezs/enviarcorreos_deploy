import smtplib

from datetime import date

from email.message import EmailMessage
from email.headerregistry import Address

from typing import List

from io import BytesIO

from pydantic import BaseModel
from jinja2 import (Environment, select_autoescape, FileSystemLoader,)

env = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())

class User(BaseModel):
    name: str
    awards: int
    matches: int
    date_joined: date = date.today()
    pals: List[str]
    show_information: bool = False

def render_html(user: User):
    template_result = env.get_template("welcome.html")
    template_result = template_result.render(user=user)
    return template_result

def open_file_image():
    file_image: BytesIO = None
    with open("rocket.png", mode="rb") as file:
        file_image = file.read()
    return file_image

def build_email(user: User):

    html_data: str = render_html(user)

    email_message = EmailMessage()
    email_message["Subject"] = "Correo de prueba"
    email_message["From"] = Address(username="lhernandezs331", domain="gmail.com", display_name="lhernandezs@sena.edu.co")
    email_message["To"] = Address(username="leo66", domain="hotmail.com", display_name="LeoHot")
    email_message.add_alternative(html_data, subtype="html")
    email_message.add_attachment(open_file_image(), maintype="image", subtype="png", filename="rocket.png")

    with open(".\\archivos\\cierre de Curso CSF - Act 2023 03 20.xlsx", "rb") as f:
        email_message.add_attachment(
            f.read(),
            filename="Cierre de Curso CSF - Act 2023 03 20.xlsx",
            maintype="application",
            subtype="xls"
        )
    
    send_email(email_message=email_message)

def send_email(email_message: EmailMessage):

    remitente = "lhernandezs331@gmail.com"
    destinatario = "leo66@hotmail.com"

    smtp = smtplib.SMTP_SSL("smtp.gmail.com")
    smtp.login(remitente, "ghpflywujadbastq")
    smtp.sendmail(remitente, destinatario, email_message.as_string())
    smtp.quit()

user = User(name="Jane Doe", awards=3, matches=5, pals=["Drake", "Josh"], show_information=True)
build_email(user=user)