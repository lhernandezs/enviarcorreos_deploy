from datos import Datos
from datetime import date

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
    fichasAlistamiento = list(filter(lambda fila: filtroFichasAlistamiento(fila), registros))
    for row in fichasAlistamiento:
        if len(row) == 12:
            # Print columns, which correspond to indices 0 and 4.
            print('%s, %s, %s, %s, %s, %s, %s' % (row[0], row[1], row[2], row[4], row[8], row[10], row[11]))

def filtroFichasAlistamiento(fila):
#    fechaActual = date.today()
    if len(fila) == 12:
        dia = int(fila[10][0:2])
        mes = int(fila[10][3:5])
        anno = int(fila[10][6:10])
        if date(2023, 6, 1) < date(anno, mes, dia):
            return True

    return False
    
if __name__ == '__main__':
    main()

