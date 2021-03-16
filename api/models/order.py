""" Holds Class Order"""

from api.models import Base
from api.models.base_model import BaseModel
from sqlalchemy import Column, Float, Boolean


class Order(BaseModel, Base):
    """Representation of an Order """

    __tablename__ = 'orders'
    total = Column(Float, nullable=False)
    sub_total = Column(Float, nullable=False)
    taxes = Column(Float, nullable=False)
    paid = Column(Boolean, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes Order"""
        super().__init__(*args, **kwargs)
