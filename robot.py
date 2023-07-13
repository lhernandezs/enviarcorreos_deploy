from datos          import Datos
from datetime       import date
from anno           import Anno
from correo         import Correo
from modelo         import Modelo

class Robot:

    def __init__(self):
        self._datosConexion = Datos("json\conexion.json") # crea una instancia de datos según el archivo JSON de la conexion
        self._datos = None

    # consigue las fichas de la hora
    def getDatos(self):
        credenciales = self._datosConexion.getCredenciales() # consigue las credenciales
        datos = self._datosConexion.getDatos(credenciales) # consigue los registros

        if not datos:
            print('No se pudo obtener los datos.')
            return
    
        self._datos = datos

    def processDatos(self):
        fechaActual = date.today()
        diasLaborables = Anno(fechaActual.year).listaDiasLaborables()

        if fechaActual in diasLaborables: # el robot solo envia correos en dias laborables

        #   # Se deja para produccion
            # indiceFechaActual = diasLaborables.index(fechaActual)
            # fichasAlistamiento = list(filter(lambda fila: filtroFichasAlistamiento(fila, fechaActual, diasLaborables[indiceFechaActual + 1], True), self._datos))

            # para prueba --  se debe quitar
            filaAlistamiento = list(filter(lambda fila: self.filtroFichasAlistamiento(fila, date(2023, 6, 21), date(2023, 6, 22), True), self._datos))
            filaAlistamiento.append( ["","","","","","","","","","","",""] ) # para procesar el ultimo bloque

            instructorAnterior = ""
            fichas = []
            for fila in filaAlistamiento:
                instructor  = fila[4]
                if not instructor == instructorAnterior:
                    if instructorAnterior != "":
                        (emailIns, seremailIns) = email.split(sep = "@")
                        user = Modelo(instructor = instructorAnterior, email = email, fichas = fichas)
                        
                        # para prueba -- se debe quitar
                        correo = Correo('sercorreoalistamiento.json','leo66', 'hotmail.com', 'LeoHotmail', user )
                        
                        #   # Se deja para produccion
                        # correo = Correo('sercorreoalistamiento.json',emailIns, seremailIns, instructor, user )
                       
                        correo.build_email(user=user)
                    instructorAnterior = instructor
                    fichas = []
                ficha       = fila[0]
                curso       = fila[1]
                familia     = fila[2]
                email       = fila[8]
                fecIni      = fila[10]
                fecFin      = fila[11]
                fichas.append([ficha, curso, familia, fecIni, fecFin])

    #  
    def filtroFichasAlistamiento(self, fila, fechaActual, fechaInicio, alistamiento):
        if len(fila) == 12:
            if alistamiento:
                dia = int(fila[10][0:2])
                mes = int(fila[10][3:5])
                anno = int(fila[10][6:10])
            else:
                dia = int(fila[11][0:2])
                mes = int(fila[11][3:5])
                anno = int(fila[11][6:10])

            if fechaActual < date(anno, mes, dia) and date(anno, mes, dia) <= fechaInicio:
                return True
        return False
    
if __name__ == '__main__':
    robot = Robot()
    datos = robot.getDatos()
    robot.processDatos()
