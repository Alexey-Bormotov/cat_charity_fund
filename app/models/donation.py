from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import CharityDonationBase


class Donation(CharityDonationBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
