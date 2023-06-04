from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator

from app.schemas.mixins import SchemasMixin


class CharityBase(BaseModel):
    class Config:
        min_anystr_length = 1
        extra = Extra.forbid


class CharityUpdate(CharityBase):
    name: Optional[str] = Field(None, max_length=100, example='patch_Charity_project_1')
    description: Optional[str] = Field(None, example='patch_description for Charity_project_1')
    full_amount: Optional[int] = Field(None, gt=0, example=10)
    # if field is present in request body it cannot be None

    @validator('name', 'description', 'full_amount')
    def field_cannot_be_null(cls, field):
        if field is None:
            raise ValueError('Поле не может быть пустым!')
        return field


class CharityCreate(CharityBase):
    name: str = Field(max_length=100, example='Charity_project_1')
    description: str = Field(example='description for Charity_project_1')
    full_amount: int = Field(gt=0, example=20)


class CharityResponse(SchemasMixin, CharityCreate):
    id: int
    create_date: dt

    class Config:
        orm_mode = True