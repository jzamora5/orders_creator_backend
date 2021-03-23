""" Holds Class User"""

from api.models import Base
from api.models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from api.utils import encrypt_password


class User(BaseModel, Base):
    """Representation of a User """

    __tablename__ = 'users'
    name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    company = Column(String(128), nullable=False)
    orders = relationship("Order",
                          backref="user",
                          cascade="all, delete, delete-orphan")

    # def __setattr__(self, name, value):
    #     """Hashes the password with bcrypt"""
    #     if name == "password":
    #         encrypted = encrypt_password.hash_password(value)
    #         value = encrypted
    #     super().__setattr__(name, value)
