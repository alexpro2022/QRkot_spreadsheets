from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas

from .base import CRUDBase


class DonationCRUD(CRUDBase[
    models.Donation,
    schemas.DonationPayload,
    schemas.DonationPayload,
]):
    async def get_user_donations(
        self, session: AsyncSession, user: models.User
    ) -> Optional[List[models.Donation]]:
        return await self.get_all_by_attr(session, 'user_id', user.id)

    async def get_open_donations(
        self, session: AsyncSession
    ) -> Optional[List[models.Donation]]:
        return await self.get_all_by_attr(session, 'fully_invested', False)


donation_crud = DonationCRUD(models.Donation)
