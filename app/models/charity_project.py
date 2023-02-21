from sqlalchemy import Column, String, Text

from app.core import Base
from app.models.mixins import CommonFieldsMixin


class CharityProject(CommonFieldsMixin, Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        return (
            f'name: {self.name}, \n'
            f'full_amount: {self.full_amount}, \n'
            f'invested_amount: {self.invested_amount}, \n'
            f'fully_invested: {self.fully_invested}, \n'
            f'close_date: {self.close_date}. \n\n'
        )