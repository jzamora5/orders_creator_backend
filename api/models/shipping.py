""" Holds Class Shipping"""

from api.models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Float


class Shipping(BaseModel, Base):
    """Representation of a Shipping """

    __tablename__ = 'shippings'
    address = Column(String(128), nullable=True)
    city = Column(String(128), nullable=True)
    state = Column(String(128), nullable=False)
    country = Column(String(128), nullable=False)
    company = Column(Float, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes Shipping"""
        super().__init__(*args, **kwargs)
