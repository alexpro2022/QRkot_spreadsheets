from typing import List

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# from app.core import db, google_client, user
from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_crud
from app.api import google_api
from app import schemas


router = APIRouter(prefix='/google', tags=['Google'])


@router.post(
    '/',
    response_model=List[schemas.CharityResponse],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service),
):
    """Только для суперюзеров."""
    projects = await charity_crud.get_projects_by_completion_rate(session)
    await google_api.upload(projects, wrapper_services)
    return projects