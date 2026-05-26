"""Pydantic schemas for FastAPI requests and responses."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models.enums import (
    AccountTypeName,
    CardStatus,
    CardType,
    CustomerGender,
    CustomerStatus,
    TransactionStatus,
    TransactionTypeName,
)


# --------------------
# Customer schemas
# --------------------


class CustomerBase(BaseModel):
    Customer_Name: str
    Customer_Lastname: str
    Customer_Email: EmailStr
    Customer_Phone: str
    Customer_Gender: CustomerGender
    Customer_BirthDate: datetime
    Customer_Status: CustomerStatus
    Customer_Country: str
    Customer_Nationality: str


class CustomerCreate(BaseModel):
    customer_id: Optional[int] = None
    name: str
    lastname: str
    email: EmailStr
    phone: str
    gender: CustomerGender
    birth_date: datetime
    status: CustomerStatus = CustomerStatus.Active
    country: str
    nationality: str
    login: str
    password: str


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    gender: Optional[CustomerGender] = None
    birth_date: Optional[datetime] = None
    status: Optional[CustomerStatus] = None
    country: Optional[str] = None
    nationality: Optional[str] = None


class CustomerOut(CustomerBase):
    Customer_ID: int

    class Config:
        orm_mode = True


# --------------------
# Account schemas
# --------------------


class AccountCreate(BaseModel):
    account_id: Optional[int] = None
    customer_id: int
    account_name: str
    account_type: AccountTypeName
    initial_balance: Decimal = Decimal("0.00")
    currency: str = "USD"
    limit_type: Optional[str] = None
    limit_max_amount: Optional[Decimal] = None


class AccountUpdate(BaseModel):
    account_name: Optional[str] = None
    account_type: Optional[AccountTypeName] = None


class AccountOut(BaseModel):
    Account_ID: int
    Customer_ID: int
    Account_Name: str
    Account_Type: AccountTypeName

    class Config:
        orm_mode = True


class BalanceOut(BaseModel):
    Balance_ID: int
    Account_ID: int
    Balance: Decimal
    Currency: str
    isLimited: bool

    class Config:
        orm_mode = True


class BalanceCreate(BaseModel):
    balance: Decimal = Decimal("0.00")
    currency: str = "USD"
    is_limited: bool = False


# --------------------
# Card schemas
# --------------------


class CardCreate(BaseModel):
    account_id: int
    card_number: str
    card_type: CardType
    expiration_date: datetime
    status: CardStatus = CardStatus.Active
    is_active: bool = True


class CardUpdate(BaseModel):
    status: Optional[CardStatus] = None
    is_active: Optional[bool] = None


class CardOut(BaseModel):
    Card_ID: int
    Account_ID: int
    Card_Number: str
    Card_Type: CardType
    Card_Expiration_Date: datetime
    Card_Status: CardStatus
    Is_Active: bool

    class Config:
        orm_mode = True


# --------------------
# Transaction schemas
# --------------------


class TransactionCreate(BaseModel):
    account_id: int
    amount: Decimal
    type_name: TransactionTypeName
    status: TransactionStatus = TransactionStatus.Created
    details: Optional[str] = None
    recipient_account_id: Optional[int] = None
    recipient_customer_id: Optional[int] = None


class TransferRequest(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: Decimal
    details: Optional[str] = None


class TransactionOut(BaseModel):
    Transaction_ID: int
    Transaction_Date: datetime
    Amount_Of_Transaction: int
    Transaction_Details: Optional[str] = None
    Account_ID: int
    Transaction_Status: TransactionStatus
    Type_ID: int
    Transaction_Recipients_Account_ID: Optional[int] = None
    Transaction_Recipients_Customer_ID: Optional[int] = None

    class Config:
        orm_mode = True

