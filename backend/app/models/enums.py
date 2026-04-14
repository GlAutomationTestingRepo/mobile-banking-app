"""Shared enum definitions for banking tables (stored as strings for SQLite/PostgreSQL)."""

from enum import Enum


class CustomerGender(str, Enum):
    M = "M"
    F = "F"


class CustomerStatus(str, Enum):
    Active = "Active"
    Inactive = "Inactive"
    Pending = "Pending"
    Suspended = "Suspended"
    Blocked = "Blocked"
    Closed = "Closed"


class AccountTypeName(str, Enum):
    Current_Main = "Current/Main"
    Savings = "Savings"
    Business = "Business"
    Joint = "Joint"


class CardType(str, Enum):
    Credit_Card = "Credit Card"
    Debit_Card = "Debit Card"


class CardStatus(str, Enum):
    Active = "Active"
    Inactive = "Inactive"
    Blocked = "Blocked"
    Expired = "Expired"
    Closed = "Closed"


class TransactionStatus(str, Enum):
    Created = "Created"
    Pending = "Pending"
    Processing = "Processing"
    Completed = "Completed"
    Failed = "Failed"
    Cancelled = "Cancelled"


class TransactionTypeName(str, Enum):
    Transfer = "Transfer"
    Payment = "Payment"
    Withdrawal = "Withdrawal"
    Deposit = "Deposit"
    Fee = "Fee"
    Refund = "Refund"


class ResetType(str, Enum):
    Password_Reset = "Password Reset"
    PIN_Reset = "PIN Reset"
    MFA_Reset = "MFA Reset"
    Username_Login_Reset = "Username/Login Reset"
