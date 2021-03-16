""" Holds Class Payment"""

from api.models import Base
from api.models.base_model import BaseModel
from sqlalchemy import Column, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Payment(BaseModel, Base):
    """Representation of a Payment """

    __tablename__ = 'payments'
    payment_type = Column(String(128), nullable=True)
    total = Column(Float, nullable=False)
    status = Column(Boolean, nullable=False)
    order_id = Column(String(60), ForeignKey('orders.id'), nullable=False)
    order = relationship("Order", back_populates="payment")

    def __init__(self, *args, **kwargs):
        """Initializes Payment"""
        super().__init__(*args, **kwargs)
