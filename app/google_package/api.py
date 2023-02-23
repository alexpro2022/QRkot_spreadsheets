from typing import List, Dict

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import (
    current_superuser,
    get_async_session,
    settings,
)
from app.crud import charity_crud
from .services import (
    clear_disk,
    get_google_service,
    get_all_spreadsheets,
    delete_spreadsheet,
    upload,
)


router = APIRouter(prefix='/google', tags=['Google'])


@router.post(
    '/',
    dependencies=[Depends(current_superuser)],
    summary='Формирование отчёта в гугл-таблице.',
    description=(
        f'{settings.SUPER_ONLY}' +
        'В таблице будут закрытые проекты, отсортированные по скорости '
        'сбора средств — от тех, что закрылись быстрее всего, до тех, '
        'что долго собирали нужную сумму.'
    ))
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_google_service),
) -> str:
    projects = await charity_crud.get_projects_by_completion_rate(session)
    return await upload(projects, wrapper_services)


@router.get(
    '/',
    dependencies=[Depends(current_superuser)],
    summary='Вывод всех отчетов.',
    description=(
        f'{settings.SUPER_ONLY}' +
        'Будет выведен список всех таблиц, хранящихся на диске, '
        'либо пустой список.'
    ))
async def get_all_spreadsheets_api(
    wrapper_services: Aiogoogle = Depends(get_google_service)
) -> List[Dict[str, str]]:
    return await get_all_spreadsheets(wrapper_services)


@router.delete(
    '/',
    dependencies=[Depends(current_superuser)],
    summary='Очистка диска.',
    description=(
        f'{settings.SUPER_ONLY}' +
        '**__ВНИМАНИЕ: с диска будут удалены все таблицы!__**'
    ))
async def clear_disk_api(
    wrapper_services: Aiogoogle = Depends(get_google_service)
) -> str:
    return await clear_disk(wrapper_services)


@router.delete(
    '/{spreadsheet_id}',
    dependencies=[Depends(current_superuser)],
    summary='Удаление таблицы.',
    description=(
        f'{settings.SUPER_ONLY}' +
        '**__Введите id таблицы, которую хотите удалить.__**'
    ))
async def delete_spreadsheet_api(
    spreadsheet_id: str,
    wrapper_services: Aiogoogle = Depends(get_google_service)
) -> str:
    return await delete_spreadsheet(spreadsheet_id, wrapper_services)
