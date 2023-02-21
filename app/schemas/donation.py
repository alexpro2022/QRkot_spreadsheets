from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, Extra, Field

from app.schemas.mixins import SchemasMixin


class DonationBase(BaseModel):
    full_amount: int = Field(gt=0)
    comment: Optional[str] = None

    class Config:
        extra = Extra.forbid


class DonationPayload(DonationBase):
    pass


class DonationResponsePartial(DonationBase):
    id: int
    create_date: dt

    class Config:
        orm_mode = True


class DonationResponseFull(SchemasMixin, DonationResponsePartial):
    user_id: int