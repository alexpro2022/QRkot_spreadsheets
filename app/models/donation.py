from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core import Base
from app.models.mixins import CommonFieldsMixin


class Donation(CommonFieldsMixin, Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self) -> str:
        return (
            f'user_id: {self.user_id}, \n'
            f'full_amount: {self.full_amount}, \n'
            f'invested_amount: {self.invested_amount}, \n'
            f'fully_invested: {self.fully_invested}, \n'
            f'close_date: {self.close_date}. \n\n'
        )