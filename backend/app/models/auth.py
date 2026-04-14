"""Auth / login credentials (one row per customer)."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.types import bigint

if TYPE_CHECKING:
    from app.models.customer import Customer


class CustomerAuth(Base):
    __tablename__ = "auth"

    CustomerID: Mapped[int] = mapped_column(
        "CustomerID",
        bigint,
        ForeignKey("customers.Customer_ID", ondelete="CASCADE"),
        primary_key=True,
    )
    Customer_Login: Mapped[str] = mapped_column("Customer_Login", String(100), unique=True, index=True)
    Customer_Password_Hash: Mapped[str] = mapped_column(
        "Customer_Password_Hash", String(255), nullable=False
    )

    customer: Mapped["Customer"] = relationship("Customer", back_populates="auth")
