from datetime import datetime as dt
from http import HTTPStatus
from typing import AsyncGenerator, Dict, List, Optional

from aiogoogle import Aiogoogle, GoogleAPI
from aiogoogle.excs import HTTPError
from fastapi import HTTPException

from app import models
from .settings import GoogleSettings


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
            'title': f'Отчет от: {__get_datetime()}',
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
        'majorDimension': GoogleSettings.DIMENSIONS,
        'values': __create_table(projects),
    }
    service = await __get_api_service(wrapper_services)
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=GoogleSettings.RANGE,
            valueInputOption=GoogleSettings.INPUT_OPTION,
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
) -> str:
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await spreadsheets_update_value(
        spreadsheet_id, projects, wrapper_services)
    return (
        f'Создан новый документ: '
        f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}')


async def get_all_spreadsheets(
    wrapper_services: Aiogoogle,
) -> List[Dict[str, str]]:
    service = await __get_api_service(wrapper_services, drive=True)
    response = await wrapper_services.as_service_account(
        service.files.list(
            q='mimeType="application/vnd.google-apps.spreadsheet"'))
    return response['files']


async def delete_spreadsheet(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle,
) -> str:
    service = await __get_api_service(wrapper_services, drive=True)
    try:
        await wrapper_services.as_service_account(
            service.files.delete(fileId=spreadsheet_id))
    except HTTPError:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f'Документ с id = {spreadsheet_id} не найден.')
    return f'Документ с id = {spreadsheet_id} удален.'


async def clear_disk(wrapper_services: Aiogoogle) -> str:
    spreadsheets = await get_all_spreadsheets(wrapper_services)
    if spreadsheets:
        for spreadsheet in spreadsheets:
            await delete_spreadsheet(spreadsheet['id'], wrapper_services)
        return 'Документы удалены, диск пуст.'
    return 'На диске нет документов для удаления.'
