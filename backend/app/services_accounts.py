"""Account, balance, and limits operations."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session

from app.models import Account, AccountLimit, AccountsBalance, AccountTypeName


def create_account(
    db: Session,
    *,
    customer_id: int,
    account_name: str,
    account_type: AccountTypeName,
    initial_balance: Decimal = Decimal("0.00"),
    currency: str = "USD",
    limit_type: Optional[str] = None,
    limit_max_amount: Optional[Decimal] = None,
    limit_start_date: Optional[datetime] = None,
    limit_expiration_date: Optional[datetime] = None,
) -> Account:
    """Create a new account with optional balance and limit."""
    account = Account(
        Customer_ID=customer_id,
        Account_Name=account_name,
        Account_Type=account_type,
    )
    db.add(account)
    db.flush()  # get Account_ID

    balance = AccountsBalance(
        Account_ID=account.Account_ID,
        Balance=initial_balance,
        Currency=currency,
        isLimited=bool(limit_type and limit_max_amount is not None),
    )
    db.add(balance)

    if limit_type and limit_max_amount is not None:
        db.add(
            AccountLimit(
                Account_ID=account.Account_ID,
                Limit_Type=limit_type,
                Limits_Max_Amount=limit_max_amount,
                Limits_Start_Date=limit_start_date or datetime.utcnow(),
                Limits_Expiration_Date=limit_expiration_date,
            )
        )

    db.commit()
    db.refresh(account)
    return account


def get_account_by_id(db: Session, account_id: int) -> Optional[Account]:
    """Return account by ID."""
    return db.get(Account, account_id)


def update_account_name(
    db: Session,
    account_id: int,
    *,
    account_name: Optional[str] = None,
    account_type: Optional[AccountTypeName] = None,
) -> Optional[Account]:
    """Update mutable account fields (name/type)."""
    account = db.get(Account, account_id)
    if not account:
        return None

    if account_name is not None:
        account.Account_Name = account_name
    if account_type is not None:
        account.Account_Type = account_type

    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def get_account_balance(
    db: Session,
    account_id: int,
) -> Optional[AccountsBalance]:
    """Return current balance row for the account (assumes one row per account)."""
    return (
        db.query(AccountsBalance)
        .filter(AccountsBalance.Account_ID == account_id)
        .order_by(AccountsBalance.Balance_ID.desc())
        .first()
    )


def list_account_balances(db: Session, account_id: int) -> list[AccountsBalance]:
    """Return all balance rows for the account (oldest -> newest)."""
    return (
        db.query(AccountsBalance)
        .filter(AccountsBalance.Account_ID == account_id)
        .order_by(AccountsBalance.Balance_ID.asc())
        .all()
    )


def create_account_balance(
    db: Session,
    *,
    account_id: int,
    balance: Decimal = Decimal("0.00"),
    currency: str = "USD",
    is_limited: bool = False,
    max_balances_per_account: int = 3,
) -> AccountsBalance:
    """Create an additional balance row for an account (max N per account)."""
    existing_count = (
        db.query(AccountsBalance).filter(AccountsBalance.Account_ID == account_id).count()
    )
    if existing_count >= max_balances_per_account:
        raise ValueError(f"Maximum {max_balances_per_account} balances per account")

    row = AccountsBalance(
        Account_ID=account_id,
        Balance=balance,
        Currency=currency,
        isLimited=is_limited,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

