from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.core import (
    calculate_investments,
    current_user,
    current_superuser,
    get_async_session
)
from app.crud import charity_crud, donation_crud
from app.models import User

router = APIRouter(prefix='/donation', tags=['Donations'])


@router.get(
    '/',
    response_model=List[schemas.DonationResponseFull],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    return await donation_crud.get_all(session)


@router.get(
    '/my',
    response_model=List[schemas.DonationResponsePartial],
    response_model_exclude_none=True,
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    return await donation_crud.get_user_donations(session, user)


@router.post(
    '/',
    response_model=schemas.DonationResponsePartial,
    response_model_exclude_none=True,
)
async def create_donation(
    payload: schemas.DonationPayload,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Сделать пожертвование."""
    new_donation = await donation_crud.create(session, payload, user)
    await calculate_investments(
        session,
        await charity_crud.get_open_projects(session),
        await donation_crud.get_open_donations(session),
    )
    await session.refresh(new_donation)
    return new_donation