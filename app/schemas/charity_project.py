from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator

from app.schemas.mixins import SchemasMixin


class CharityBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    full_amount: Optional[int] = Field(None, gt=0)

    class Config:
        min_anystr_length = 1
        extra = Extra.forbid


class CharityUpdate(CharityBase):
    @validator('name', 'description', 'full_amount')
    def field_cannot_be_null(cls, field):
        if field is None:
            raise ValueError('Поле не может быть пустым!')
        return field


class CharityCreate(CharityBase):
    name: str = Field(max_length=100)
    description: str
    full_amount: int = Field(gt=0)


class CharityResponse(SchemasMixin, CharityCreate):
    id: int
    create_date: dt

    class Config:
        orm_mode = True