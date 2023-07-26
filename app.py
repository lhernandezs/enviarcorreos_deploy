
import smtplib
import os.path
import json
import os

from email.message          import EmailMessage
from email.headerregistry   import Address
from modelo                 import Salida
from jinja2                 import (Environment, select_autoescape, FileSystemLoader,)

from robot import Robot
from fastapi import FastAPI 

ENV = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape()) # variable de entorno para la API de jinja2

app = FastAPI()

@app.get("/")
def read_root():
    return({"welcome":"hola, saludos a todos, bendiciones"})

@app.get("/execRobot/{pw}")
def execRobot(pw: str):
    produc = False
    if produc:
        robot = Robot(produccion = True, passw = pw)
    else:
        robot = Robot(produccion = False, passw = pw)
    robot.getDatos()
    robot.processDatos()

    file = os.path.join("log", "salida.log")
    with open(file, mode="r", encoding="ISO-8859-1") as file:
        texto = file.readlines()
        file.close()
    salida = Salida(reporte=texto)

    template_result = ENV.get_template("salida.html").render(user=salida)

    with open(os.path.join('json', 'sercorreoalistamiento.json'), 'r') as conex:
        arc = json.load(conex)
        conex.close()

    emaEnv = arc["emailRemitente"] 
    serEnv = arc["servidorRemitente"] 
    namEnv = arc["nombreRemitente"] 

    email_message               = EmailMessage()
    email_message["Subject"]    = "archivo de salida"
    email_message["From"]       = Address(username = emaEnv, domain = serEnv, display_name = namEnv)
    email_message["To"]         = Address(username="lhernandezs", domain="sena.edu.co", display_name="LeonardoTo")

    email_message.add_alternative(template_result, subtype="html")
    
    remitente = emaEnv + "@" + serEnv
    destinatarios = [ "lhernandezs@sena.edu.co"]

    smtp = smtplib.SMTP_SSL("smtp.gmail.com")
    smtp.login(remitente, pw) # para que gmail pueda enviar correos desde un aplicativo externo se requiere una clave de 16 caracteres

    smtp.sendmail(remitente, destinatarios, email_message.as_string())
    smtp.quit()

    return ({"texto": texto})
