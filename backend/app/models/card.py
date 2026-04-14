"""Cards table."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import CardStatus, CardType
from app.models.types import bigint

if TYPE_CHECKING:
    from app.models.account import Account


class Card(Base):
    __tablename__ = "cards"

    Card_ID: Mapped[int] = mapped_column(
        "Card_ID", bigint, primary_key=True, autoincrement=True
    )
    Account_ID: Mapped[int] = mapped_column(
        "Account_ID",
        ForeignKey("accounts.Account_ID", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    Card_Number: Mapped[str] = mapped_column("Card_Number", String(16), nullable=False)
    Card_Type: Mapped[CardType] = mapped_column(
        SQLEnum(CardType, native_enum=False, length=20), nullable=False
    )
    Card_Expiration_Date: Mapped[datetime] = mapped_column(
        "Card_Expiration_Date", DateTime(timezone=True), nullable=False
    )
    Card_Status: Mapped[CardStatus] = mapped_column(
        SQLEnum(CardStatus, native_enum=False, length=20), nullable=False
    )
    Is_Active: Mapped[bool] = mapped_column("Is_Active", Boolean, default=True, nullable=False)

    account: Mapped["Account"] = relationship("Account", back_populates="cards")
