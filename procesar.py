from datos import fichas
from datetime import date

def main():

    SCOPES          = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    HOJA            = '1yEIyw5cmIOA2-TsY1dqo4dZerVdjvm5qIalFf9cOi8w'
    RANGO           = 'formacion!A7:L1000'
    CREDENCIALES    = 'credentials.json'
    TOKEN           = 'token.json'
    PATH            = 'json'

    fichas = fichas(SCOPES, HOJA, RANGO, CREDENCIALES, TOKEN, PATH) 
    credenciales = fichas.obtenerCredenciales()
    registros = fichas.obtenerDatos(credenciales)

    if not registros:
        print('No se pudo obtener los datos.')
        return

    fechaActual = date.today()
    
    fichasAlistamiento = list(filter(lambda f: len(f) == 12 and date(2023, 6, 1) < date(int(f[10][6:10]), int(f[10][3:5]), int(f[10][0:2])) , registros))

    for row in fichasAlistamiento:
        if len(row) == 12:
            # Print columns, which correspond to indices 0 and 4.
            print('%s, %s, %s, %s, %s, %s, %s, %s' % (row[0], row[1], row[2], row[4], row[8], row[10], row[11], fechaActual))

if __name__ == '__main__':
    main()

