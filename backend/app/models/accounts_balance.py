"""Accounts_Balance table."""

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.types import bigint

if TYPE_CHECKING:
    from app.models.account import Account


class AccountsBalance(Base):
    __tablename__ = "accounts_balance"

    Balance_ID: Mapped[int] = mapped_column(
        "Balance_ID", bigint, primary_key=True, autoincrement=True
    )
    Account_ID: Mapped[int] = mapped_column(
        "Account_ID",
        ForeignKey("accounts.Account_ID", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    Balance: Mapped[Decimal] = mapped_column("Balance", Numeric(15, 2), nullable=False)
    Currency: Mapped[str] = mapped_column("Currency", String(13), nullable=False)
    isLimited: Mapped[bool] = mapped_column("isLimited", Boolean, default=False, nullable=False)

    account: Mapped["Account"] = relationship("Account", back_populates="balances")
