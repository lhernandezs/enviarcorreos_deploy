import time
import random
import os
 
from datos          import Datos
from datetime       import date, datetime
from anno           import Anno
from correo         import Correo
from modelo         import Modelo
from log            import Log
class Robot:

    def __init__(self, produccion = False):
        self._produccion = produccion
        self._datosConexion = Datos(os.path.join("json", "conexion.json")) # crea una instancia de datos según el archivo de configuracion JSON de la conexion
        self._datos = None

    # consigue las fichas de la hora
    def getDatos(self):
        credenciales = self._datosConexion.getCredenciales() # consigue las credenciales
        datos = self._datosConexion.getDatos(credenciales) # consigue los registros

        if not datos: 
            Log('No se pudo cargar los datos', tipo="Error")
            return
    
        self._datos = datos

    # filtra las filas si tienen los datos de fechaInicio/Terminacion segun la fecha de inicio / terminacion 
    def filtroFichas(self, fila, fechaActual, fechaLabSig, alistamiento):
        if len(fila) == 12:
            indice = 10 if alistamiento else 11
            (anno, mes, dia) = (int(fila[indice][6:10]), int(fila[indice][3:5]), int(fila[indice][0:2]))
            if fechaActual < date(anno, mes, dia) and date(anno, mes, dia) <= fechaLabSig: return True
        return False

    # envia los correos segun las filas 
    def sendCorreos(self, filas, agregarArchivo):
        instructorAnterior = ""
        fichas = []
        for fila in filas:
            instructor  = fila[4]
            if not instructor == instructorAnterior:
                if instructorAnterior != "":

                    if self._produccion: time.sleep(random.randint(60, 240)) # detiene la ejeucón del envio de correo por unos segundo
                    
                    (emailIns, seremailIns) = email.split(sep = "@")
                    strFichas = ""
                    for nf in fichas: strFichas += nf[0] + ", "
                    user = Modelo(instructor = instructorAnterior, email = email, fichas = fichas, agregarArchivo = agregarArchivo)
                    archivoJson = 'sercorreoterminacion.json' if agregarArchivo else 'sercorreoalistamiento.json'

                    if not self._produccion:
                        correo = Correo(archivoJson,'leo66', 'hotmail.com', 'LeoHotmail', user )  # para prueba 
                    else:
                        correo = Correo(archivoJson, emailIns, seremailIns, instructor, user ) # para produccion

                    Log("Se envio correo de " + ("Terminacion" if agregarArchivo else "Alistamiento") + " a " + instructorAnterior + " con " + str(len(fichas)) + " fichas: [ " + strFichas +"]")
                    correo.build_email(user=user)

                instructorAnterior = instructor
                fichas = []

            (ficha, curso, familia, email, fecIni, fecFin) = (fila[0], fila[1], fila[2], fila[8], fila[10], fila[11],)
            fichas.append([ficha, curso, familia, fecIni, fecFin])
            
    # revisa si el dia de envio de correos es laborable, filtra las fichas y llama a sendCorreos()
    def processDatos(self):
        if self._datos:
            fechaActual = date.today()
            diasLaborables = Anno(fechaActual.year).listaDiasLaborables()

            Log("NUEVA EJECUCION DEL ROBOT", "+++++")
            if fechaActual in diasLaborables or not self._produccion: # el robot solo envia correos en dias laborables en producion

                if not self._produccion: fechaActual = date(2023, 6, 22) # para pruebas
                fechaLabSig = diasLaborables[diasLaborables.index(fechaActual) + 1]

                # append(["" for i in range(12)]) para procesar el ultimo instructor
                filasAlistamiento = (list(filter(lambda fila: self.filtroFichas(fila, fechaActual, fechaLabSig, True), self._datos)))
                filasAlistamiento.append(["" for i in range(12)]) 
                filasTerminacion  = (list(filter(lambda fila: self.filtroFichas(fila, fechaActual, fechaLabSig, False), self._datos)))
                filasTerminacion.append(["" for i in range(12)]) 

                if (cantidad := len(filasAlistamiento)) > 1:
                    Log("Hay " + str(cantidad - 1) + " fichas de Alistamiento")
                    self.sendCorreos(filasAlistamiento, False)
                else:
                    Log("No hay fichas para Alistamiento")

                if (cantidad := len(filasTerminacion)) > 1: 
                    Log("Hay " + str(cantidad - 1) + " fichas de Terminacion")
                    self.sendCorreos(filasTerminacion, True)
                else:
                    Log("No hay fichas para Terminacion")
            else:
                Log("Solo se ejecuta en dias laborables (en produccion)")


if __name__ == '__main__':
    robot = Robot()
    # para produccion se debe cambiar los correos y nombre del Coordinador en los archivos servcorreoalistamiento y servcorreoterminacion
    # robot = Robot(produccion = True)
    robot.getDatos()
    robot.processDatos()
