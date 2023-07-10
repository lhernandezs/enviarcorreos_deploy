from email.message import EmailMessage
import smtplib


remitente = "lhernandezs331@gmail.com"
destinatario = "leo66@hotmail.com"
mensaje = "<h1>¡Hola, mundo 2!</h1>"
email = EmailMessage()
email["From"] = remitente
email["To"] = destinatario
email["Subject"] = "Correo de prueba"
email.set_content(mensaje, subtype="html")
with open("Cierre de Curso CSF - Act 2023 03 20.xlsx", "rb") as f:
    email.add_attachment(
        f.read(),
        filename="Cierre de Curso CSF - Act 2023 03 20.xlsx",
        maintype="application",
        subtype="xls"
    )

smtp = smtplib.SMTP_SSL("smtp.gmail.com")
smtp.login(remitente, "ghpflywujadbastq")
smtp.sendmail(remitente, destinatario, email.as_string())
smtp.quit()