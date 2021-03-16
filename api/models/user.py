""" Holds Class User"""

from api.models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class User(BaseModel, Base):
    """Representation of a User """

    __tablename__ = 'users'
    name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    company = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes User"""
        super().__init__(*args, **kwargs)
