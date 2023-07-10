import smtplib
import os.path

from datetime import date
from email.message import EmailMessage
from email.headerregistry import Address
from typing import List
from io import BytesIO
from pydantic import BaseModel
from jinja2 import (Environment, select_autoescape, FileSystemLoader,)

class Modelo(BaseModel):
    name: str
    awards: int
    matches: int
    date_joined: date = date.today()
    pals: List[str]
    show_information: bool = False

class Correo:

    ENV = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())

    def __init__(self, emaEnv, emaRec, serEnv, serRec, namEnv, namRec, asunto, templa, modelo, adjunt,):
        self._emaEnv = emaEnv
        self._emaRec = emaRec
        self._serEnv = serEnv
        self._serRec = serRec
        self._namEnv = namEnv
        self._namRec = namRec
        self._asunto = asunto
        self._templa = templa
        self._modelo = modelo
        self._adjunt = adjunt


    def render_html(self, modelo: Modelo):
        template_result = Correo.ENV.get_template(self._templa)
        template_result = template_result.render(user=modelo)
        return template_result

    def open_file(self):
        file_image: BytesIO = None
        with open(self._adjunt, mode="rb") as file:
            file_image = file.read()
        return file_image

    def build_email(self, user: Modelo):

        html_data: str = self.render_html(user)

        email_message               = EmailMessage()
        email_message["Subject"]    = self._asunto
        email_message["From"]       = Address(username=self._emaEnv, domain=self._serEnv, display_name=self._namEnv)
        email_message["To"]         = Address(username=self._emaRec, domain=self._serRec, display_name=self._namRec)
        email_message.add_alternative(html_data, subtype="html")
        email_message.add_attachment(self.open_file(), maintype="application", subtype="xls", filename=self._adjunt)
        
        self.send_email(email_message=email_message)

    def send_email(self, email_message: EmailMessage):

        remitente = self._emaEnv + "@" + self._serEnv
        destinatario = self._emaRec + "@" + self._serRec

        smtp = smtplib.SMTP_SSL("smtp.gmail.com")
        smtp.login(remitente, "ghpflywujadbastq")
        smtp.sendmail(remitente, destinatario, email_message.as_string())
        smtp.quit()

user = Modelo(name="Juliana", awards=3, matches=5, pals=["Darwin", "Dana"], show_information=True)
correo = Correo("lhernandezs331","leo66", "gmail.com", "hotmail.com","LeoGmail", "LeoHotmail", "pruebaCorreo", "welcome.html", user, os.path.join("attachments","cierre de Curso CSF - Act 2023 03 20.xlsx"))
correo.build_email(user=user)