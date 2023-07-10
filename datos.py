import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class fichas:

    def __init__(self, scopes, hoja, rango, credenciales, token, path):
        self._scopes = scopes
        self._hoja = hoja
        self._rango = rango
        self._credenciales = credenciales
        self._token = token
        self._path = path

    def obtenerCredenciales(self):

        # El archivo token.json almacena los tokens de acceso y actualización del usuario, y se crea automáticamente cuando el flujo de autorización se completa por primera vez.
        token = os.path.join(self._path, self._token)
        credenciales = os.path.join(self._path, self._credenciales)
        creds = None

        if os.path.exists(token):
            creds = Credentials.from_authorized_user_file(token, self._scopes)

        # Si no hay credenciales (válidas) disponibles, permite que el usuario inicie sesión.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credenciales, self._scopes)
                creds = flow.run_local_server(port=0)
            
            # Guarde las credenciales para la próxima ejecución
            with open(token, 'w') as token:
                token.write(creds.to_json())
        
        return creds

    def obtenerDatos(self, creds):
        try:
            service = build('sheets', 'v4', credentials=creds)

            # Llamar a la Sheets API y cargar los datos
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self._hoja, range=self._rango).execute()
            return result.get('values', [])

        except HttpError as err:
            print(err)
