from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.core import (calculate_investments, current_superuser,
                      get_async_session, settings)
from app.crud import charity_crud, donation_crud

router = APIRouter(prefix='/charity_project', tags=['Charity Projects'])


@router.get(
    '/',
    response_model=List[schemas.CharityResponse],
    response_model_exclude_none=True,
    summary='Возвращает список всех проектов.',
    description=(
        f'{settings.ALL_USERS}' +
        'Возвращает список всех проектов.'
    ))
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_crud.get_all(session)


@router.post(
    '/',
    response_model=schemas.CharityResponse,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Создание благотворительного проекта.',
    description=(
        f'{settings.SUPER_ONLY}' +
        'Создаёт благотворительный проект.'
    ))
async def create_charity_project(
    payload: schemas.CharityCreate,
    session: AsyncSession = Depends(get_async_session),
):
    new_project = await charity_crud.create(session, payload)
    await calculate_investments(
        session,
        await charity_crud.get_open_projects(session),
        await donation_crud.get_open_donations(session),
    )
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=schemas.CharityResponse,
    dependencies=[Depends(current_superuser)],
    summary='Редактирование проекта.',
    description=(
        f'{settings.SUPER_ONLY}' +
        'Закрытый проект нельзя редактировать. '
        'Нельзя установить требуемую сумму меньше уже вложенной.'
    ))
async def update_charity_project(
    project_id: int,
    payload: schemas.CharityUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    updated = await charity_crud.update(session, project_id, payload)
    await calculate_investments(session, updated)
    await session.refresh(updated)
    return updated


@router.delete(
    '/{project_id}',
    response_model=schemas.CharityResponse,
    dependencies=[Depends(current_superuser)],
    summary='Удаление проекта.',
    description=(
        f'{settings.SUPER_ONLY}' +
        'Удаляет проект. Нельзя удалить проект, '
        'в который уже были инвестированы средства, '
        'его можно только закрыть.'
    ))
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_crud.delete(session, project_id)