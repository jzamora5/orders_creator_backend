""" Holds Class Shipping"""

from api.models import Base
from api.models.base_model import BaseModel
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class Shipping(BaseModel, Base):
    """Representation of a Shipping """

    __tablename__ = 'shippings'
    address = Column(String(128), nullable=True)
    city = Column(String(128), nullable=True)
    state = Column(String(128), nullable=False)
    country = Column(String(128), nullable=False)
    cost = Column(Float, nullable=False)
    order_id = Column(String(60), ForeignKey(
        'orders.id'), nullable=False)
    order = relationship("Order", back_populates="shipping")

    def __init__(self, *args, **kwargs):
        """Initializes Shipping"""
        super().__init__(*args, **kwargs)
