from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel


class SchemasMixin(BaseModel):
    invested_amount: int
    fully_invested: bool
    close_date: Optional[dt] = None