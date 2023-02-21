from datetime import datetime as dt
from typing import List, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession

from app import models


def __get_balance(
    obj: Union[models.CharityProject, models.Donation]
) -> None:

    return obj.full_amount - obj.invested_amount


def __close_object(
    obj: Union[models.CharityProject, models.Donation],
) -> None:

    obj.invested_amount = obj.full_amount
    obj.fully_invested = True
    obj.close_date = dt.now()


def __calc(
    less: Union[models.CharityProject, models.Donation],
    greater: Union[models.CharityProject, models.Donation],
) -> None:

    greater.invested_amount += __get_balance(less)
    __close_object(less)


async def calculate_investments(
    session: AsyncSession,
    projects: Union[List[models.CharityProject], models.CharityProject],
    donations: Optional[List[models.Donation]] = None,
) -> None:

    if projects and donations:
        project_id, donation_id = 0, 0
        while project_id < len(projects) and donation_id < len(donations):
            project_balance = __get_balance(projects[project_id])
            donation_balance = __get_balance(donations[donation_id])
            if donation_balance < project_balance:
                __calc(donations[donation_id], projects[project_id])
                donation_id += 1
            elif project_balance < donation_balance:
                __calc(projects[project_id], donations[donation_id])
                project_id += 1
            else:
                __close_object(donations[donation_id])
                donation_id += 1
                __close_object(projects[project_id])
                project_id += 1
        await session.commit()

    elif isinstance(projects, models.CharityProject):
        if projects.invested_amount == projects.full_amount:
            __close_object(projects)
            await session.commit()