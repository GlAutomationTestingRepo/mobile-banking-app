"""Customers table."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum as SQLEnum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import CustomerGender, CustomerStatus
from app.models.types import bigint

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.auth import CustomerAuth
    from app.models.reset_verify import ResetVerify
    from app.models.transaction import Transaction


class Customer(Base):
    __tablename__ = "customers"

    Customer_ID: Mapped[int] = mapped_column(
        "Customer_ID", bigint, primary_key=True, autoincrement=True
    )
    Customer_Name: Mapped[str] = mapped_column("Customer_Name", String(50), nullable=False)
    Customer_Lastname: Mapped[str] = mapped_column("Customer_Lastname", String(50), nullable=False)
    Customer_Email: Mapped[str] = mapped_column("Customer_Email", String(100), unique=True, index=True)
    Customer_Phone: Mapped[str] = mapped_column("Customer_Phone", String(20), nullable=False)
    Customer_Gender: Mapped[CustomerGender] = mapped_column(
        SQLEnum(CustomerGender, native_enum=False, length=5), nullable=False
    )
    Customer_BirthDate: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    Customer_DateCreated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    Customer_Status: Mapped[CustomerStatus] = mapped_column(
        SQLEnum(CustomerStatus, native_enum=False, length=20), nullable=False
    )
    Customer_Country: Mapped[str] = mapped_column("Customer_Country", String(100), nullable=False)
    Customer_Nationality: Mapped[str] = mapped_column(
        "Customer_Nationality", String(100), nullable=False
    )

    accounts: Mapped[list["Account"]] = relationship(
        "Account", back_populates="customer", cascade="all, delete-orphan"
    )
    auth: Mapped["CustomerAuth | None"] = relationship(
        "CustomerAuth", back_populates="customer", uselist=False, cascade="all, delete-orphan"
    )
    reset_verify_tokens: Mapped[list["ResetVerify"]] = relationship(
        "ResetVerify", back_populates="customer", cascade="all, delete-orphan"
    )
    recipient_transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        foreign_keys="Transaction.Transaction_Recipients_Customer_ID",
        back_populates="recipient_customer",
    )
