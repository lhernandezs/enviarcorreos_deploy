import os
from datetime import datetime

class Log: 

    def __init__(self, mensaje, tipo = "Aviso"):
        file = os.path.join("log", "salida.log")
        with open(file, mode="a+") as file:
            texto = '\n' + tipo + " -- " + str(mensaje).ljust(120,'.') + str(datetime.now())
            file.write(texto)
            file.close()