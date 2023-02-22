from datetime import datetime as dt
from typing import AsyncGenerator, List, Optional

from aiogoogle import Aiogoogle, GoogleAPI
from aiogoogle.auth.creds import ServiceAccountCreds

from app import models
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


async def get_google_service() -> AsyncGenerator[Aiogoogle, None]:
    async with Aiogoogle(
        service_account_creds=GoogleSettings.CREDENTIALS
    ) as aiogoogle:
        yield aiogoogle


async def __get_api_service(
    wrapper_services: Aiogoogle,
    drive: bool = False,
) -> GoogleAPI:
    if drive:
        return await wrapper_services.discover(
            GoogleSettings.DRIVE_API_NAME,
            GoogleSettings.DRIVE_API_VERSION,
        )
    return await wrapper_services.discover(
        GoogleSettings.SHEETS_API_NAME,
        GoogleSettings.SHEETS_API_VERSION,
    )


def __get_datetime() -> str:
    return dt.now().strftime(GoogleSettings.FORMAT)


def __create_table(
    projects: Optional[List[models.CharityProject]],
) -> List[List[str]]:
    table = [
        ['Отчет от', __get_datetime()],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание'],
    ]
    if projects:
        for project in projects:
            table.append([
                project.name,
                str(project.close_date - project.create_date),
                project.description,
            ])
    return table


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    spreadsheet_body = {
        'properties': {
            'title': f'Отчет от {__get_datetime()}',
            'locale': GoogleSettings.LOCALE,
        },
        'sheets': GoogleSettings.SHEETS_PROPERTIES,
    }
    service = await __get_api_service(wrapper_services)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body))
    return response['spreadsheetId']


async def spreadsheets_update_value(
    spreadsheet_id: str,
    projects: Optional[List[models.CharityProject]],
    wrapper_services: Aiogoogle
) -> None:
    update_body = {
        'majorDimension': 'ROWS',
        'values': __create_table(projects),
    }
    service = await __get_api_service(wrapper_services)
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body,
        ))


async def set_user_permissions(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle,
) -> None:
    service = await __get_api_service(wrapper_services, drive=True)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=GoogleSettings.PERMISSIONS_BODY,
            fields=GoogleSettings.PERMISSIONS_FIELDS,
        ))


async def upload(
    projects: List[models.CharityProject],
    wrapper_services: Aiogoogle,
) -> None:
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(
        spreadsheetid, projects, wrapper_services,
    )