"""
Create all tables from SQLAlchemy models.

Run from the `backend` folder:
    python init_db.py
"""

from app.database import engine
from app.models import Base  # noqa: F401
from app.models import (  # noqa: F401
    Account,
    AccountLimit,
    AccountsBalance,
    Card,
    Customer,
    CustomerAuth,
    ResetVerify,
    Transaction,
    TransactionHistory,
    TransactionType,
)


def main() -> None:
    Base.metadata.create_all(bind=engine)
    print("Tables created (or already exist):", sorted(Base.metadata.tables.keys()))


if __name__ == "__main__":
    main()
