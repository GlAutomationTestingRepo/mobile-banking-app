"""Import all models so metadata knows every table (migrations / create_all)."""

from app.models.account import Account
from app.models.account_limit import AccountLimit
from app.models.accounts_balance import AccountsBalance
from app.models.auth import CustomerAuth
from app.models.base import Base
from app.models.card import Card
from app.models.customer import Customer
from app.models.enums import (
    AccountTypeName,
    CardStatus,
    CardType,
    CustomerGender,
    CustomerStatus,
    ResetType,
    TransactionStatus,
    TransactionTypeName,
)
from app.models.reset_verify import ResetVerify
from app.models.retired_id import RetiredAccountId, RetiredCustomerId
from app.models.transaction import Transaction
from app.models.transaction_history import TransactionHistory
from app.models.transaction_type import TransactionType

__all__ = [
    "Base",
    "Account",
    "AccountLimit",
    "AccountsBalance",
    "Card",
    "Customer",
    "CustomerAuth",
    "ResetVerify",
    "RetiredAccountId",
    "RetiredCustomerId",
    "Transaction",
    "TransactionHistory",
    "TransactionType",
    "AccountTypeName",
    "CardStatus",
    "CardType",
    "CustomerGender",
    "CustomerStatus",
    "ResetType",
    "TransactionStatus",
    "TransactionTypeName",
]
