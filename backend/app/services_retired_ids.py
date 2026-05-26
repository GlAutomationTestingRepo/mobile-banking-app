"""Track and enforce non-reuse of deleted customer and account IDs."""

from sqlalchemy.orm import Session

from app.models import Account, RetiredAccountId, RetiredCustomerId


def is_customer_id_retired(db: Session, customer_id: int) -> bool:
    return db.get(RetiredCustomerId, customer_id) is not None


def is_account_id_retired(db: Session, account_id: int) -> bool:
    return db.get(RetiredAccountId, account_id) is not None


def ensure_customer_id_available(db: Session, customer_id: int) -> None:
    if is_customer_id_retired(db, customer_id):
        raise ValueError(
            f"Customer_ID {customer_id} was previously deleted and cannot be reused"
        )


def ensure_account_id_available(db: Session, account_id: int) -> None:
    if is_account_id_retired(db, account_id):
        raise ValueError(
            f"Account_ID {account_id} was previously deleted and cannot be reused"
        )


def retire_customer_id(db: Session, customer_id: int) -> None:
    if not is_customer_id_retired(db, customer_id):
        db.add(RetiredCustomerId(Customer_ID=customer_id))


def retire_account_id(db: Session, account_id: int) -> None:
    if not is_account_id_retired(db, account_id):
        db.add(RetiredAccountId(Account_ID=account_id))


def retire_accounts_for_customer(db: Session, customer_id: int) -> None:
    account_ids = (
        db.query(Account.Account_ID).filter(Account.Customer_ID == customer_id).all()
    )
    for (account_id,) in account_ids:
        retire_account_id(db, account_id)
