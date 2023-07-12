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
        # fechaActual = date.today()
        # diasLaborables = Anno(fechaActual.year).listaDiasLaborables()
        # if fechaActual in diasLaborables: # el robot solo envia correos en dias laborables
        #     indiceFechaActual = diasLaborables.index(fechaActual)

        #     # para prueba --  se debe quitar
        #     fichasAlistamiento = list(filter(lambda fila: self.filtroFichasAlistamiento(fila, date(2023, 6, 21), date(2023, 6, 22), True), self._datos))
            
        #     # Se deja para produccion
        #     # fichasAlistamiento = list(filter(lambda fila: filtroFichasAlistamiento(fila, fechaActual, diasLaborables[indiceFechaActual + 1], True), self._datos))

        #     for row in fichasAlistamiento:
        #         if len(row) == 12:
        #             # Print columns, which correspond to indices 0 and 4.
        #             print('%s, %s, %s, %s, %s, %s, %s' % (row[0], row[1], row[2], row[4], row[8], row[10], row[11]))

        #    user = Modelo(name="Juliana", awards=3, matches=5, pals=["Darwin", "Dana"], show_information=True)

            user = Modelo(instructor="Juliana", email="juli@hotmail.com", fichas=[("hola 1", 1),("que mas 2", 3)], show_information=True)

            correo = Correo('sercorreo.json','leo66', 'hotmail.com', 'LeoHotmail', user )
            correo.build_email(user=user)

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
#    robot.getDatos()
    robot.processDatos()
