# print('22/06/2023'[6:10])
# print('22/06/2023'[3:5])
# print('22/06/2023'[0:2])

# import os
# import json
# path = "json"

# lista = [n for n in range(1,5)]
# while i:= lista.pop(0):
#     print(i)

# cadena = "leo66@hotmail.com"
# (dir, ser) = cadena.split(sep="@")
# print(dir)
# print(ser)

# adjunto = "attachments/cierre de Curso CSF - Act 2023 03 20.xlsx"
# print(adjunto.split(sep="/")[1])

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

username = "lhernandezs@sena.edu.co"
password = "nala2709.060501"
mail_from = "lhernandezs@sena.edu.co"
mail_to = "leo66@hotmail.com"
mail_subject = "prueba"
mail_body = "This is a test message"

mimemsg = MIMEMultipart()
mimemsg['From']=mail_from
mimemsg['To']=mail_to
mimemsg['Subject']=mail_subject
mimemsg.attach(MIMEText(mail_body, 'plain'))
connection = smtplib.SMTP(host='smtp.office365.com', port=587)
connection.starttls()
connection.login(username,password)
connection.send_message(mimemsg)
connection.quit()
