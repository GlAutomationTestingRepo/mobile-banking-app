"""Transaction and transfer operations."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session

from app.models import (
    Account,
    AccountsBalance,
    Transaction,
    TransactionHistory,
    TransactionStatus,
    TransactionType,
    TransactionTypeName,
)


def _get_balance_row_for_update(db: Session, account_id: int) -> Optional[AccountsBalance]:
    return (
        db.query(AccountsBalance)
        .filter(AccountsBalance.Account_ID == account_id)
        .order_by(AccountsBalance.Balance_ID.desc())
        .with_for_update()
        .first()
    )


def _get_transaction_type_id(db: Session, type_name: TransactionTypeName) -> int:
    type_row = db.query(TransactionType).filter(TransactionType.Type_Name == type_name).first()
    if not type_row:
        # Create it lazily if it doesn't exist yet.
        type_row = TransactionType(Type_Name=type_name)
        db.add(type_row)
        db.flush()
    return type_row.Type_ID


def create_transaction(
    db: Session,
    *,
    account_id: int,
    amount: Decimal,
    type_name: TransactionTypeName,
    status: TransactionStatus = TransactionStatus.Created,
    details: Optional[str] = None,
    recipient_account_id: Optional[int] = None,
    recipient_customer_id: Optional[int] = None,
) -> Transaction:
    """Create a transaction record only (no balance changes)."""
    type_id = _get_transaction_type_id(db, type_name)
    tx = Transaction(
        Amount_Of_Transaction=int(amount),
        Transaction_Details=details,
        Account_ID=account_id,
        Transaction_Status=status,
        Type_ID=type_id,
        Transaction_Recipients_Account_ID=recipient_account_id,
        Transaction_Recipients_Customer_ID=recipient_customer_id,
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def transfer_money(
    db: Session,
    *,
    from_account_id: int,
    to_account_id: int,
    amount: Decimal,
    details: Optional[str] = None,
) -> Transaction:
    """Transfer money between two accounts with balance, limits and history updates."""
    if amount <= 0:
        raise ValueError("Amount must be positive")

    from_account = db.get(Account, from_account_id)
    to_account = db.get(Account, to_account_id)
    if not from_account or not to_account:
        raise ValueError("Invalid account IDs")

    # Lock balance rows for update.
    from_balance = _get_balance_row_for_update(db, from_account_id)
    to_balance = _get_balance_row_for_update(db, to_account_id)
    if not from_balance or not to_balance:
        raise ValueError("Balance not found for one of the accounts")

    # Basic balance check.
    if Decimal(from_balance.Balance) < amount:
        raise ValueError("Insufficient funds")

    # Very simple limit check: if account is limited, ensure amount <= max limit.
    for limit in from_account.limits:
        if limit.Limits_Expiration_Date and limit.Limits_Expiration_Date < datetime.utcnow():
            continue
        if amount > Decimal(limit.Limits_Max_Amount):
            raise ValueError("Amount exceeds account limit")

    # Prepare transaction as Pending first.
    type_id = _get_transaction_type_id(db, TransactionTypeName.Transfer)
    tx = Transaction(
        Amount_Of_Transaction=int(amount),
        Transaction_Details=details,
        Account_ID=from_account_id,
        Transaction_Status=TransactionStatus.Pending,
        Type_ID=type_id,
        Transaction_Recipients_Account_ID=to_account_id,
        Transaction_Recipients_Customer_ID=to_account.Customer_ID,
    )
    db.add(tx)
    db.flush()

    history_created = TransactionHistory(
        Transaction_ID=tx.Transaction_ID,
        History_Satus_Before=None,
        History_Status_After=TransactionStatus.Pending,
        History_Created_By=None,
    )
    db.add(history_created)

    # Apply balance updates.
    from_balance.Balance = Decimal(from_balance.Balance) - amount
    to_balance.Balance = Decimal(to_balance.Balance) + amount

    # Mark transaction as Completed.
    previous_status = tx.Transaction_Status
    tx.Transaction_Status = TransactionStatus.Completed
    db.add(tx)

    history_completed = TransactionHistory(
        Transaction_ID=tx.Transaction_ID,
        History_Satus_Before=previous_status,
        History_Status_After=TransactionStatus.Completed,
        History_Created_By=None,
    )
    db.add(history_completed)

    db.commit()
    db.refresh(tx)
    return tx


def get_transaction_history(
    db: Session,
    *,
    account_id: Optional[int] = None,
    customer_id: Optional[int] = None,
) -> list[Transaction]:
    """Return transactions filtered by account or recipient customer."""
    query = db.query(Transaction)
    if account_id is not None:
        query = query.filter(Transaction.Account_ID == account_id)
    if customer_id is not None:
        query = query.filter(Transaction.Transaction_Recipients_Customer_ID == customer_id)
    return query.order_by(Transaction.Transaction_Date.desc()).all()


def cancel_transaction(
    db: Session,
    *,
    transaction_id: int,
) -> Optional[Transaction]:
    """Cancel a transaction and (naively) reverse balance changes if it was completed."""
    tx = db.get(Transaction, transaction_id)
    if not tx:
        return None

    if tx.Transaction_Status == TransactionStatus.Completed and tx.Transaction_Recipients_Account_ID:
        # Reverse transfer.
        from_balance = _get_balance_row_for_update(db, tx.Account_ID)
        to_balance = _get_balance_row_for_update(db, tx.Transaction_Recipients_Account_ID)
        if from_balance and to_balance:
            amount = Decimal(tx.Amount_Of_Transaction)
            # Reverse: move money back.
            to_balance.Balance = Decimal(to_balance.Balance) - amount
            from_balance.Balance = Decimal(from_balance.Balance) + amount

    previous_status = tx.Transaction_Status
    tx.Transaction_Status = TransactionStatus.Cancelled

    history = TransactionHistory(
        Transaction_ID=tx.Transaction_ID,
        History_Satus_Before=previous_status,
        History_Status_After=TransactionStatus.Cancelled,
        History_Created_By=None,
    )
    db.add(history)

    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

