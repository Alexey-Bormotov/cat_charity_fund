from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field


class DonationBase(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationDBPartial(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBFull(DonationDBPartial):
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    close_date: datetime = Field(None)
