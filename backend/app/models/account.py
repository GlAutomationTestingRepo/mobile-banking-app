"""Accounts table."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import AccountTypeName
from app.models.types import bigint

if TYPE_CHECKING:
    from app.models.account_limit import AccountLimit
    from app.models.accounts_balance import AccountsBalance
    from app.models.card import Card
    from app.models.customer import Customer
    from app.models.transaction import Transaction


class Account(Base):
    __tablename__ = "accounts"

    Account_ID: Mapped[int] = mapped_column(
        "Account_ID", bigint, primary_key=True, autoincrement=True
    )
    Customer_ID: Mapped[int] = mapped_column(
        "Customer_ID",
        ForeignKey("customers.Customer_ID", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    Account_Name: Mapped[str] = mapped_column("Account_Name", String(200), nullable=False)
    Account_Date_Created: Mapped[datetime] = mapped_column(
        "Account_Date_Created", DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    Account_Type: Mapped[AccountTypeName] = mapped_column(
        SQLEnum(AccountTypeName, native_enum=False, length=30), nullable=False
    )

    customer: Mapped["Customer"] = relationship("Customer", back_populates="accounts")
    balances: Mapped[list["AccountsBalance"]] = relationship(
        "AccountsBalance", back_populates="account", cascade="all, delete-orphan"
    )
    cards: Mapped[list["Card"]] = relationship(
        "Card", back_populates="account", cascade="all, delete-orphan"
    )
    limits: Mapped[list["AccountLimit"]] = relationship(
        "AccountLimit", back_populates="account", cascade="all, delete-orphan"
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        back_populates="account",
        foreign_keys="Transaction.Account_ID",
    )
    recipient_transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction",
        foreign_keys="Transaction.Transaction_Recipients_Account_ID",
        back_populates="recipient_account",
        overlaps="transactions,account,recipient_account",
    )
