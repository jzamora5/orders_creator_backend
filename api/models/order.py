""" Holds Class Order"""

from api.models import Base
from api.models.base_model import BaseModel
from api.models.payment import Payment
from sqlalchemy import Column, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from api.utils.sort import mergeSort


TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


class Order(BaseModel, Base):
    """Representation of an Order """

    __tablename__ = 'orders'
    total = Column(Float, nullable=False)
    sub_total = Column(Float, nullable=False)
    taxes = Column(Float, nullable=False)
    paid = Column(Boolean, nullable=False, default=False)
    status = Column(String(60), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    shipping = relationship("Shipping", uselist=False, back_populates="order")
    payments = relationship("Payment",
                            backref="order",
                            cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initializes Order"""
        super().__init__(*args, **kwargs)

    def to_dict(self):
        new_dict = super().to_dict()
        shipping = self.shipping
        user = self.user
        payments = self.payments

        if shipping:
            new_dict["shipping_info"] = shipping.to_dict()
        else:
            new_dict["shipping_info"] = "Not Available"

        if user:
            user_dict = user.to_dict()
            user_dict.pop("orders", None)
            new_dict["customer_id"] = user_dict.pop("id")
            new_dict["customer_name"] = user_dict.pop("name")

            new_dict["user_information"] = user_dict

        else:
            new_dict["user_information"] = "Not Available"

        list_payments = []
        for payment in payments:
            list_payments.append(payment.to_dict())

        if list_payments:
            mergeSort(list_payments, ["created_at"])
            new_dict["last_payment_date"] = payments[-1].created_at.strftime(
                TIME_FORMAT)
        else:
            new_dict["last_payment_date"] = "Not Available"

        new_dict.pop("user", None)
        new_dict.pop("shipping", None)

        return new_dict
