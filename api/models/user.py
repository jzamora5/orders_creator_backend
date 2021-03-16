""" Holds Class User"""

from api.models import Base
from api.models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a User """

    __tablename__ = 'users'
    name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    company = Column(String(128), nullable=False)
    orders = relationship("Order",
                          backref="user",
                          cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes User"""
        super().__init__(*args, **kwargs)
