"""IDs that were deleted and must never be reused."""

from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.models.types import bigint


class RetiredCustomerId(Base):
    __tablename__ = "retired_customer_ids"

    Customer_ID: Mapped[int] = mapped_column("Customer_ID", bigint, primary_key=True)
    Retired_At: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class RetiredAccountId(Base):
    __tablename__ = "retired_account_ids"

    Account_ID: Mapped[int] = mapped_column("Account_ID", bigint, primary_key=True)
    Retired_At: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
