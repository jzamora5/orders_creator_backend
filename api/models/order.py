""" Holds Class Order"""

from api.models import Base
from api.models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship


class Order(BaseModel, Base):
    """Representation of an Order """

    __tablename__ = 'orders'
    total = Column(Float, nullable=False)
    sub_total = Column(Float, nullable=False)
    taxes = Column(Float, nullable=False)
    paid = Column(Boolean, nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    shipping = relationship("Shipping", uselist=False, back_populates="order")
    payment = relationship("Payment", uselist=False, back_populates="order")

    def __init__(self, *args, **kwargs):
        """Initializes Order"""
        super().__init__(*args, **kwargs)
