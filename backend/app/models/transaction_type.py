"""Transaction_Type lookup table."""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum as SQLEnum, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import TransactionTypeName
from app.models.types import bigint

if TYPE_CHECKING:
    from app.models.transaction import Transaction


class TransactionType(Base):
    __tablename__ = "transaction_type"

    Type_ID: Mapped[int] = mapped_column(
        "Type_ID", bigint, primary_key=True, autoincrement=True
    )
    Type_Name: Mapped[TransactionTypeName] = mapped_column(
        SQLEnum(TransactionTypeName, native_enum=False, length=30), nullable=False, unique=True
    )
    Type_Description: Mapped[str | None] = mapped_column("Type_Description", Text, nullable=True)
    Type_Fee: Mapped[Decimal | None] = mapped_column("Type_Fee", Numeric(15, 2), nullable=True)
    Type_Created_At: Mapped[datetime] = mapped_column(
        "Type_Created_At", DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="transaction_type"
    )
