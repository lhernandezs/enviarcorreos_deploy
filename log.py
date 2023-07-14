import os
from datetime import datetime

class Log:    
    def __init__(self, mensaje, tipo = "Aviso"):
        diaYHora = datetime.now()
        file = os.path.join("log", "errores.log")
        with open(file, mode="a+") as file:
            texto = '\n' + tipo + " -- " + str(mensaje).ljust(120,'.') + str(diaYHora)
            file.write(texto)
            file.close()