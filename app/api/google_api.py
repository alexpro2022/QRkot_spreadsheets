from datetime import datetime as dt
from typing import List

from aiogoogle import Aiogoogle

from app.core.config import settings
from app import models

FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    properties = {
        'title': f'Отчет от {dt.now().strftime(FORMAT)}',
        'locale': 'ru_RU',
    }
    sheets = [{
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
    spreadsheet_body = {'properties': properties, 'sheets': sheets}
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body))
    return response['spreadsheetId']


async def set_user_permissions(
    spreadsheetid: str,
    wrapper_services: Aiogoogle,
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email,
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields='id',
        )
    )


async def spreadsheets_update_value(
    spreadsheetid: str,
    projects: List[models.CharityProject],
    wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчет от', dt.now().strftime(FORMAT)],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание'],
    ]
    if projects:
        for project in projects:
            table_values.append([
                project.name,
                str(project.close_date - project.create_date),
                project.description,
            ])

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values,
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body,
        )
    )


async def upload(
    projects: List[models.CharityProject],
    wrapper_services: Aiogoogle,
) -> None:
    spreadsheetid = await spreadsheets_create(wrapper_services)
    # print(f'https://docs.google.com/spreadsheets/d/{spreadsheetid}')
    await set_user_permissions(spreadsheetid, wrapper_services)
    await spreadsheets_update_value(
        spreadsheetid, projects, wrapper_services,
    )
