from datos      import Datos
from datetime   import date
from anno       import Anno

def main():

    registros = getRegistros()
    procesarRegistros(registros)

def getRegistros():
    registros = Datos("json\conexion.json") # crea una instancia de datos según el archivo JSON de la conexion
    credenciales = registros.getCredenciales() # consigue las credenciales
    registros = registros.getDatos(credenciales) # consigue los registros

    if not registros:
        print('No se pudo obtener los datos.')
        return
   
    return registros

def procesarRegistros(registros):
    fechaActual = date.today()
    diasLaborables = Anno(fechaActual.year).listaDiasLaborables()
    if fechaActual in diasLaborables: # el robot solo envia correos en dias laborables
        indiceFechaActual = diasLaborables.index(fechaActual)

        # para prueba --  se debe quitar
        fichasAlistamiento = list(filter(lambda fila: filtroFichasAlistamiento(fila, date(2023, 6, 21), date(2023, 6, 22), True), registros))
        
        # Se deja para produccion
        fichasAlistamiento = list(filter(lambda fila: filtroFichasAlistamiento(fila, fechaActual, diasLaborables[indiceFechaActual + 1], True), registros))

        for row in fichasAlistamiento:
            if len(row) == 12:
                # Print columns, which correspond to indices 0 and 4.
                print('%s, %s, %s, %s, %s, %s, %s' % (row[0], row[1], row[2], row[4], row[8], row[10], row[11]))

def filtroFichasAlistamiento(fila, fechaActual, fechaInicio, alistamiento):
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
    main()

