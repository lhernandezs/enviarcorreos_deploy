import os.path
import json

from google.auth.transport.requests     import Request
from google.oauth2.credentials          import Credentials
from google_auth_oauthlib.flow          import InstalledAppFlow
from googleapiclient.discovery          import build
from googleapiclient.errors             import HttpError
from log                                import Log
from os import remove

class Datos:

    # constructor de la clase
    def __init__(self, archivoJson):

        # leo el archivo JSON para obtener los datos de conexion a la hoja de calculo
        with open(archivoJson, 'r') as conex:
            arc = json.load(conex)
            conex.close()

        self._scopes        = arc["scopes"] 
        self._hoja          = arc["hoja"] 
        self._rango         = arc["rango"] 
        self._credenciales  = arc["credenciales"] 
        self._token         = arc["token"] 
        self._path          = arc["path"]

    # consigo el token y/o credenciales de conexion
    def getCredenciales(self):
        # El archivo token.json almacena los tokens de acceso y actualización del usuario, y se crea automáticamente cuando el flujo de autorización se completa por primera vez.
        token = os.path.join(self._path, self._token)
        credenciales = os.path.join(self._path, self._credenciales)
        creds = None

        try:
            
            if os.path.exists(token):
                creds = Credentials.from_authorized_user_file(token, self._scopes)

        # Si no hay credenciales (válidas) disponibles, permite que el usuario inicie sesión.

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(credenciales, self._scopes)
                    creds = flow.run_local_server(port=0)
                
                # Guarda las credenciales para la próxima ejecución
                with open(token, 'w') as token:
                    token.write(creds.to_json())
        except:
            remove(token)
            creds = Credentials.from_authorized_user_file(token, self._scopes)
            creds.refresh(Request())

            flow = InstalledAppFlow.from_client_secrets_file(credenciales, self._scopes)
            creds = flow.run_local_server(port=0)

            with open(token, 'w') as token:
                token.write(creds.to_json())

        return creds

    # obtengo los datos de las fichas o None si no es posible la conexión
    def getDatos(self, creds):
        try:
            service = build('sheets', 'v4', credentials=creds)

            # Llama a la Sheets API y cargar los datos
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self._hoja, range=self._rango).execute()
            return result.get('values', [])

        except HttpError as err:
            Log(err)
            return None

if __name__ == "__main__":
    datos = Datos(os.path.join("json", "conexion.json"))
    c = datos.getCredenciales()
    d = datos.getDatos(c)
    for fila in d:
        print(fila)
