"""Limits table (named AccountLimit in Python — `limits` is reserved in SQL contexts)."""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.types import bigint

if TYPE_CHECKING:
    from app.models.account import Account


class AccountLimit(Base):
    __tablename__ = "limits"

    Limits_ID: Mapped[int] = mapped_column(
        "Limits_ID", bigint, primary_key=True, autoincrement=True
    )
    Account_ID: Mapped[int] = mapped_column(
        "Account_ID",
        ForeignKey("accounts.Account_ID", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    Limit_Type: Mapped[str] = mapped_column("Limit_Type", String(50), nullable=False)
    Limits_Max_Amount: Mapped[Decimal] = mapped_column(
        "Limits_Max_Amount", Numeric(15, 2), nullable=False
    )
    Limits_Start_Date: Mapped[datetime] = mapped_column(
        "Limits_Start_Date", DateTime(timezone=True), nullable=False
    )
    Limits_Expiration_Date: Mapped[datetime | None] = mapped_column(
        "Limits_Expiration_Date", DateTime(timezone=True), nullable=True
    )

    account: Mapped["Account"] = relationship("Account", back_populates="limits")
