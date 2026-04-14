"""Transactions table."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import TransactionStatus
from app.models.types import bigint

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.customer import Customer
    from app.models.transaction_history import TransactionHistory
    from app.models.transaction_type import TransactionType


class Transaction(Base):
    __tablename__ = "transactions"

    Transaction_ID: Mapped[int] = mapped_column(
        "Transaction_ID", bigint, primary_key=True, autoincrement=True
    )
    Transaction_Date: Mapped[datetime] = mapped_column(
        "Transaction_Date", DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    Amount_Of_Transaction: Mapped[int] = mapped_column(
        "Amount_Of_Transaction", bigint, nullable=False
    )
    Transaction_Details: Mapped[str | None] = mapped_column(
        "Transaction_Details", String(500), nullable=True
    )
    Account_ID: Mapped[int] = mapped_column(
        "Account_ID",
        ForeignKey("accounts.Account_ID", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    Transaction_Status: Mapped[TransactionStatus] = mapped_column(
        SQLEnum(TransactionStatus, native_enum=False, length=20), nullable=False
    )
    Type_ID: Mapped[int] = mapped_column(
        "Type_ID",
        ForeignKey("transaction_type.Type_ID", ondelete="RESTRICT"),
        index=True,
        nullable=False,
    )
    Transaction_Recipients_Account_ID: Mapped[int | None] = mapped_column(
        "Transaction_Recipients_Account_ID",
        ForeignKey("accounts.Account_ID", ondelete="SET NULL"),
        nullable=True,
    )
    Transaction_Recipients_Customer_ID: Mapped[int | None] = mapped_column(
        "Transaction_Recipients_Customer_ID",
        ForeignKey("customers.Customer_ID", ondelete="SET NULL"),
        nullable=True,
    )

    account: Mapped["Account"] = relationship(
        "Account",
        back_populates="transactions",
        foreign_keys=[Account_ID],
    )
    recipient_account: Mapped["Account | None"] = relationship(
        "Account",
        foreign_keys=[Transaction_Recipients_Account_ID],
        back_populates="recipient_transactions",
        overlaps="account,transactions,recipient_transactions",
    )
    recipient_customer: Mapped["Customer | None"] = relationship(
        "Customer",
        foreign_keys=[Transaction_Recipients_Customer_ID],
        back_populates="recipient_transactions",
    )
    transaction_type: Mapped["TransactionType"] = relationship(
        "TransactionType", back_populates="transactions"
    )
    history_entries: Mapped[list["TransactionHistory"]] = relationship(
        "TransactionHistory", back_populates="transaction", cascade="all, delete-orphan"
    )
