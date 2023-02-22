from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import current_superuser, get_async_session
from app.crud import charity_crud
from app.google_services import get_google_service, upload


router = APIRouter(prefix='/google', tags=['Google'])


@router.post('/', dependencies=[Depends(current_superuser)])
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_google_service),
) -> str:
    """Только для суперюзеров."""
    projects = await charity_crud.get_projects_by_completion_rate(session)
    return await upload(projects, wrapper_services)