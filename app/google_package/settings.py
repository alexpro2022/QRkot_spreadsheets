from aiogoogle.auth.creds import ServiceAccountCreds

from app.core import settings


class GoogleSettings:
    FORMAT = "%Y/%m/%d %H:%M:%S"
    LOCALE = 'ru_RU'
    DRIVE_API_NAME = 'drive'
    DRIVE_API_VERSION = 'v3'
    SHEETS_API_NAME = 'sheets'
    SHEETS_API_VERSION = 'v4'
    SHEETS_PROPERTIES = [{
        'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': 'Лист1',
            'gridProperties': {
                'rowCount': 100,
                'columnCount': 11
            }
        }
    }]
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    INFO = {
        'type': settings.type,
        'project_id': settings.project_id,
        'private_key_id': settings.private_key_id,
        'private_key': settings.private_key,
        'client_email': settings.client_email,
        'client_id': settings.client_id,
        'auth_uri': settings.auth_uri,
        'token_uri': settings.token_uri,
        'auth_provider_x509_cert_url': settings.auth_provider_x509_cert_url,
        'client_x509_cert_url': settings.client_x509_cert_url
    }
    CREDENTIALS = ServiceAccountCreds(scopes=SCOPES, **INFO)
    PERMISSIONS_BODY = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email,
    }
    PERMISSIONS_FIELDS = 'id'
    DIMENSIONS = 'ROWS'
    RANGE = 'A1:E30'
    INPUT_OPTION = 'USER_ENTERED'