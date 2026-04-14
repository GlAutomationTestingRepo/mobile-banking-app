"""Reset / verify tokens (password, PIN, MFA, login)."""

from typing import TYPE_CHECKING

from sqlalchemy import Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import ResetType
from app.models.types import bigint

if TYPE_CHECKING:
    from app.models.customer import Customer


class ResetVerify(Base):
    __tablename__ = "reset_verify"

    Reset_ID: Mapped[int] = mapped_column(
        "Reset_ID", bigint, primary_key=True, autoincrement=True
    )
    Customer_ID: Mapped[int] = mapped_column(
        "Customer_ID",
        ForeignKey("customers.Customer_ID", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    Token_Hash: Mapped[int] = mapped_column("Token_Hash", bigint, nullable=False)
    Reset_Type: Mapped[ResetType] = mapped_column(
        SQLEnum(ResetType, native_enum=False, length=40), nullable=False
    )

    customer: Mapped["Customer"] = relationship("Customer", back_populates="reset_verify_tokens")
