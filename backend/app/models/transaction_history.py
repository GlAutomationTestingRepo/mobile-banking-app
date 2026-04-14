"""Transaction_History table."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import TransactionStatus
from app.models.types import bigint

if TYPE_CHECKING:
    from app.models.transaction import Transaction


class TransactionHistory(Base):
    __tablename__ = "transaction_history"

    History_ID: Mapped[int] = mapped_column(
        "History_ID", bigint, primary_key=True, autoincrement=True
    )
    Transaction_ID: Mapped[int] = mapped_column(
        "Transaction_ID",
        ForeignKey("transactions.Transaction_ID", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    History_Satus_Before: Mapped[TransactionStatus | None] = mapped_column(
        "History_Satus_Before", SQLEnum(TransactionStatus, native_enum=False, length=20), nullable=True
    )
    History_Status_After: Mapped[TransactionStatus | None] = mapped_column(
        "History_Status_After", SQLEnum(TransactionStatus, native_enum=False, length=20), nullable=True
    )
    History_Canged_At: Mapped[datetime] = mapped_column(
        "History_Canged_At", DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    History_Created_By: Mapped[int | None] = mapped_column(
        "History_Created_By", bigint, nullable=True
    )

    transaction: Mapped["Transaction"] = relationship(
        "Transaction", back_populates="history_entries"
    )
