from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.core import (calculate_investments, current_superuser, current_user,
                      get_async_session, settings)
from app.crud import charity_crud, donation_crud
from app.models import User

router = APIRouter(prefix='/donation', tags=['Donations'])


@router.get(
    '/',
    response_model=List[schemas.DonationResponseFull],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary='Возвращает список пожертвований.',
    description=(
        f'{settings.SUPER_ONLY}' +
        'Возвращает список пожертвований.'
    ))
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_all(session)


@router.get(
    '/my',
    response_model=List[schemas.DonationResponsePartial],
    response_model_exclude_none=True,
    summary='Возвращает все пожертвования выполняющего запрос пользователя.',
    description=(
        f'{settings.AUTH_ONLY}' +
        'Возвращает список пожертвований пользователя, выполняющего запрос.'
    ))
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    return await donation_crud.get_user_donations(session, user)


@router.post(
    '/',
    response_model=schemas.DonationResponsePartial,
    response_model_exclude_none=True,
    summary='Сделать пожертвование.',
    description=(
        f'{settings.AUTH_ONLY}' +
        'Сделать пожертвование.'
    ))
async def create_donation(
    payload: schemas.DonationPayload,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(session, payload, user)
    await calculate_investments(
        session,
        await charity_crud.get_open_projects(session),
        await donation_crud.get_open_donations(session),
    )
    await session.refresh(new_donation)
    return new_donation