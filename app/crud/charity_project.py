from http import HTTPStatus
from typing import Dict, List, Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.crud.base import CRUDBase


class CharityCRUD(CRUDBase[
    models.CharityProject,
    schemas.CharityCreate,
    schemas.CharityUpdate,
]):
    OBJECT_ALREADY_EXISTS = 'Проект с таким именем уже существует!'

    def is_delete_allowed(self, obj: models.CharityProject) -> None:
        if obj.invested_amount:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                'В проект были внесены средства, не подлежит удалению!',)

    def is_update_allowed(
        self, obj: models.CharityProject, payload: Dict
    ) -> None:
        if obj.fully_invested:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                'Закрытый проект нельзя редактировать!')

        if payload.get(
            'full_amount', obj.invested_amount
        ) < obj.invested_amount:
            raise HTTPException(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                'Нельзя указывать сумму меньше уже внесённой')

    def has_permission(
        self, obj: models.CharityProject, user: models.User
    ) -> None:
        pass

    async def get_open_projects(
        self, session: AsyncSession
    ) -> Optional[List[models.CharityProject]]:
        return await self.get_all_by_attr(session, 'fully_invested', False)

    async def get_closed_projects(
        self, session: AsyncSession
    ) -> Optional[List[models.CharityProject]]:
        return await self.get_all_by_attr(session, 'fully_invested', True)

    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> Optional[List[models.CharityProject]]:
        projects = await self.get_closed_projects(session)
        return sorted(
            projects,
            key=lambda project: project.close_date - project.create_date,
        )


charity_crud = CharityCRUD(models.CharityProject)
